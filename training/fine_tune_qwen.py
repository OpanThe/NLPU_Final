# Fine-tune Qwen 2.5 3B for conversational behavior
# Optimized for RTX 3050 6GB GPU with LoRA

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
    Trainer
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from dataclasses import dataclass
from typing import Dict, Sequence
import transformers

from transformers import EarlyStoppingCallback

# =========================
# CONFIGURATION
# =========================
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
OUTPUT_DIR = "./models/jarvis-qwen-finetuned"
TRAINING_DATA = "./training/fine_tuning_data.jsonl"

# =========================
# QUANTIZATION CONFIG (4-bit for 6GB GPU)
# =========================
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# =========================
# LOAD MODEL & TOKENIZER
# =========================
print(f"[*] Loading {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Qwen-specific: Set padding token (Qwen uses eos_token for padding)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# Prepare model for k-bit training
model = prepare_model_for_kbit_training(model)
print("[OK] Model loaded and prepared for training")

# =========================
# LORA CONFIGURATION
# =========================
lora_config = LoraConfig(
    r=16,                           # LoRA rank (higher = more capacity, more memory)
    lora_alpha=32,                  # Scaling factor (usually 2*r)
    target_modules=[                # Qwen 2.5 attention & MLP modules
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
        "gate_proj", "up_proj", "down_proj"       # MLP
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# =========================
# LOAD TRAINING DATA
# =========================
print("[*] Loading training data...")
dataset = load_dataset("json", data_files=TRAINING_DATA, split="train")
dataset = dataset.train_test_split(test_size=0.1, seed=42)
print(f"[OK] Loaded {len(dataset['train'])} training examples, {len(dataset['test'])} validation examples")

# =========================
# DATA FORMATTING
# =========================
def format_qwen_prompt(example):
    """Format data using Qwen 2.5's native chat template for better performance"""
    # Data is already in messages format: {"messages": [{"role": ..., "content": ...}]}
    messages = example["messages"]
    
    # Use Qwen's native chat template (automatically handles <|im_start|>, <|im_end|>)
    formatted = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False
    )
    
    return {"text": formatted}

# Apply formatting
dataset = dataset.map(format_qwen_prompt, remove_columns=dataset["train"].column_names)
print("[OK] Data formatted for Qwen 2.5")

# =========================
# TOKENIZATION
# =========================
def tokenize_function(examples):
    """Tokenize with assistant-only loss masking (Qwen optimized)"""
    tokenized = tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,  # Increased from 384 (Qwen supports 32K, safe to use 512)
        padding=False,
        return_tensors=None,
        add_special_tokens=False  # Chat template already added them
    )
    
    # Create labels (copy of input_ids)
    tokenized["labels"] = tokenized["input_ids"].copy()
    
    return tokenized

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["text"]
)
print("[OK] Data tokenized")

# =========================
# CUSTOM DATA COLLATOR (Assistant-only loss)
# =========================
@dataclass
class DataCollatorForCompletionOnlyLM:
    """Collator that masks prompt tokens (only compute loss on assistant response)"""
    tokenizer: transformers.PreTrainedTokenizer
    assistant_token_id: int = None  # Will be set in __post_init__
    
    def __post_init__(self):
        # Qwen assistant marker: "<|im_start|>assistant\n"
        self.assistant_marker = "<|im_start|>assistant"
        # Pre-tokenize to get token ID for faster masking
        self.assistant_token_ids = self.tokenizer.encode(self.assistant_marker, add_special_tokens=False)
    
    def __call__(self, instances: Sequence[Dict]) -> Dict[str, torch.Tensor]:
        input_ids = [torch.tensor(instance["input_ids"]) for instance in instances]
        labels = [torch.tensor(instance["labels"]) for instance in instances]
        
        # Pad sequences
        input_ids = torch.nn.utils.rnn.pad_sequence(
            input_ids, batch_first=True, padding_value=self.tokenizer.pad_token_id
        )
        labels = torch.nn.utils.rnn.pad_sequence(
            labels, batch_first=True, padding_value=-100
        )
        
        # Mask prompt tokens (only train on assistant response) - IMPROVED VERSION
        for i in range(len(labels)):
            # Find assistant marker position by searching token IDs (faster than decoding)
            input_ids_list = input_ids[i].tolist()
            assistant_start = -1
            
            # Search for assistant token sequence
            for j in range(len(input_ids_list) - len(self.assistant_token_ids)):
                if input_ids_list[j:j+len(self.assistant_token_ids)] == self.assistant_token_ids:
                    assistant_start = j + len(self.assistant_token_ids)
                    # Skip to content after "\n" (newline after assistant marker)
                    while assistant_start < len(input_ids_list) and input_ids_list[assistant_start] != self.tokenizer.encode("\n", add_special_tokens=False)[0]:
                        assistant_start += 1
                    assistant_start += 1  # Skip the newline token itself
                    break
            
            # Mask everything before assistant response
            if assistant_start > 0:
                labels[i, :assistant_start] = -100
        
        # Mask padding tokens
        labels[labels == self.tokenizer.pad_token_id] = -100
        
        return {
            "input_ids": input_ids,
            "attention_mask": input_ids.ne(self.tokenizer.pad_token_id),
            "labels": labels
        }

data_collator = DataCollatorForCompletionOnlyLM(tokenizer=tokenizer)

# =========================
# EVALUATION METRICS
# =========================
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(eval_preds):
    """
    Compute evaluation metrics during training:
    - Token Accuracy: How often model predicts correct token
    - Perplexity: Measure of prediction confidence (lower = better)
    - Precision/Recall/F1: Quality metrics for token predictions
    """
    predictions, labels = eval_preds
    
    # predictions shape: (batch_size, seq_len, vocab_size)
    # Get predicted token IDs (argmax over vocab dimension)
    if len(predictions.shape) == 3:
        predictions = np.argmax(predictions, axis=-1)
    
    # Flatten predictions and labels for metrics computation
    predictions_flat = predictions.flatten()
    labels_flat = labels.flatten()
    
    # Remove padding tokens (label = -100)
    mask = labels_flat != -100
    predictions_filtered = predictions_flat[mask]
    labels_filtered = labels_flat[mask]
    
    # Calculate metrics
    metrics = {}
    
    # 1. Token Accuracy: % of correctly predicted tokens
    if len(predictions_filtered) > 0:
        accuracy = accuracy_score(labels_filtered, predictions_filtered)
        metrics["token_accuracy"] = accuracy
        
        # 2. Precision, Recall, F1 (weighted average across all tokens)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels_filtered, 
            predictions_filtered,
            average='weighted',
            zero_division=0
        )
        metrics["precision"] = precision
        metrics["recall"] = recall
        metrics["f1_score"] = f1
    
    return metrics

print("[OK] Evaluation metrics configured")

# =========================
# TRAINING ARGUMENTS (Optimized for 6GB GPU)
# =========================
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=2,      # Small batch for 6GB GPU
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,      # Effective batch size = 2*8 = 16
    gradient_checkpointing=True,        # Save memory
    
    # IMPROVED: Better learning rate and scheduler for Qwen
    learning_rate=2e-4,                 # Slightly higher for better convergence
    lr_scheduler_type="cosine",
    warmup_steps=35,                    # Optimized for 250 examples (~10-15% of total steps)
    weight_decay=0.01,                  # Add weight decay for regularization
    
    # Logging and evaluation
    logging_steps=5,                    # More frequent logging with larger dataset
    logging_first_step=True,            # Log first step for debugging
    eval_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=2,
    
    # Precision and optimization
    fp16=False,                         # Use bf16 instead
    bf16=True,                          # Better for training stability
    optim="paged_adamw_8bit",           # Memory-efficient optimizer
    
    # Improved gradient settings
    max_grad_norm=0.5,                  # Increased from 0.3 for better stability
    
    # Model selection
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,            # Lower loss is better
    
    # Misc
    report_to="none",                   # Disable wandb/tensorboard
    seed=42,                            # Reproducibility
    dataloader_num_workers=0,           # Prevent multiprocessing issues on Windows
    
    # Enhanced logging
    logging_strategy="steps",
    eval_steps=None,                    # Evaluate at end of each epoch
    save_steps=None                     # Save at end of each epoch
)

# =========================
# TRAINER
# =========================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]  # Stop if no improvement for 2 epochs
)

print("[OK] Trainer initialized with metrics tracking and early stopping")

# =========================
# TRAIN
# =========================
print("\n" + "="*80)
print("[START] QWEN 2.5 3B FINE-TUNING")
print("="*80)
print(f"Training samples: {len(tokenized_dataset['train'])}")
print(f"Validation samples: {len(tokenized_dataset['test'])}")
print(f"[INFO] Effective batch size: {training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps}")
print(f"[INFO] Total epochs: {training_args.num_train_epochs}")
print(f"Metrics tracked: Loss, Accuracy, Precision, Recall, F1, Perplexity")
print(f"Early stopping: Enabled (patience=2 epochs)")
print("="*80 + "\n")

training_result = trainer.train()

# Print training summary
print("\n" + "="*80)
print("📊 TRAINING SUMMARY")
print("="*80)
print(f"⏱️  Total training time: {training_result.metrics.get('train_runtime', 0):.2f} seconds")
print(f" Final training loss: {training_result.metrics.get('train_loss', 0):.4f}")
print("="*80 + "\n")

# =========================
# SAVE MODEL
# =========================
print("\n💾 Saving fine-tuned model...")
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("\n" + "="*80)
print("✅ FINE-TUNING COMPLETE!")
print(f"📁 Model saved to: {OUTPUT_DIR}")
print("="*80 + "\n")

# Print final metrics with enhanced formatting
metrics = trainer.evaluate()
print("[METRICS] FINAL EVALUATION RESULTS:")
print("-" * 80)
for key, value in sorted(metrics.items()):
    if key == "eval_loss":
        print(f"  {key:.<30} {value:.4f}")
    elif "accuracy" in key:
        print(f"  {key:.<30} {value*100:.2f}%")
    elif key in ["eval_runtime", "eval_samples_per_second", "eval_steps_per_second"]:
        print(f"  {key:.<30} {value:.2f}")
    else:
        print(f"  {key:.<30} {value:.4f}")

# Calculate and display perplexity
import math
perplexity = math.exp(metrics["eval_loss"])
print("-" * 80)
print(f"\n[PERPLEXITY]: {perplexity:.2f}")
print("   (Lower is better - Target: < 3.0, Excellent: < 2.0)")

if "eval_token_accuracy" in metrics:
    print(f"\n[TOKEN ACCURACY]: {metrics['eval_token_accuracy']*100:.2f}%")
    print("   (Higher is better - Target: > 60%, Excellent: > 70%)")

if "eval_f1_score" in metrics:
    print(f"\n[F1 SCORE]: {metrics['eval_f1_score']:.4f}")
    print("   (Higher is better - Target: > 0.60, Excellent: > 0.70)")

print("\n" + "="*80)
print("[READY] MODEL READY FOR INFERENCE!")
print("="*80)
