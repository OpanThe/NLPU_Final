import json
import torch
from dataclasses import dataclass
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    EarlyStoppingCallback
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Configuration
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"  # Change to your model
OUTPUT_DIR = "./models/jarvis-llama-finetuned"
TRAINING_DATA = "./training/fine_tuning_data.jsonl"

# Load dataset
print("Loading training data...")
data = []
with open(TRAINING_DATA, 'r', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

# Format data for instruction tuning
def format_prompt(example):
    """Format chat messages into Llama 3.2 chat format"""
    messages = example['messages']
    formatted = "<|begin_of_text|>"
    
    for msg in messages:
        role = msg['role']
        content = msg['content']
        formatted += f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>"
    
    return formatted

# Prepare dataset
formatted_data = [{"text": format_prompt(item)} for item in data]
dataset = Dataset.from_list(formatted_data)

# Split into train/eval (225 train, 25 eval for 250 examples)
train_test_split = dataset.train_test_split(test_size=0.1, seed=42)
train_dataset = train_test_split['train']
eval_dataset = train_test_split['test']

print(f"Total dataset size: {len(dataset)} examples")
print(f"Training set: {len(train_dataset)} examples")
print(f"Evaluation set: {len(eval_dataset)} examples")
print("\nExample prompt:")
print(dataset[0]['text'][:300] + "...")

# Quantization config for 4-bit training (saves memory)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load model and tokenizer
print("\nLoading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
    use_cache=False  # Disable KV cache for training (saves memory)
)

# Prepare model for k-bit training
model = prepare_model_for_kbit_training(model)

# Enable gradient checkpointing for memory efficiency
model.gradient_checkpointing_enable()

# LoRA configuration
lora_config = LoraConfig(
    r=16,  # LoRA rank
    lora_alpha=32,  # LoRA alpha
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA to model
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Tokenize dataset - process individually to avoid batching issues
def tokenize_function(example):
    """Tokenize with loss masking - only compute loss on assistant responses"""
    text = example["text"]
    
    # Tokenize full text
    tokenized = tokenizer(
        text,
        truncation=True,
        max_length=512,  # Increased for better context
        padding=False
    )
    
    input_ids = tokenized["input_ids"]
    attention_mask = tokenized["attention_mask"]
    
    # Create labels with masking
    labels = input_ids.copy()
    
    # Find the assistant response start - search in truncated tokens
    assistant_token = "<|start_header_id|>assistant<|end_header_id|>"
    assistant_header_tokens = tokenizer.encode(assistant_token, add_special_tokens=False)
    
    # Find assistant start position in the TOKENIZED input
    assistant_start = None
    for i in range(len(input_ids) - len(assistant_header_tokens) + 1):
        if input_ids[i:i+len(assistant_header_tokens)] == assistant_header_tokens:
            assistant_start = i + len(assistant_header_tokens)
            break
    
    # Mask everything before assistant response
    if assistant_start is not None and assistant_start < len(labels):
        labels[:assistant_start] = [-100] * assistant_start
    else:
        labels = [-100] * len(labels)
    
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels
    }

print("\nTokenizing dataset with assistant-only loss masking...")
train_tokenized = train_dataset.map(
    tokenize_function, 
    remove_columns=["text"],
    desc="Tokenizing training set"
)

eval_tokenized = eval_dataset.map(
    tokenize_function,
    remove_columns=["text"],
    desc="Tokenizing evaluation set"
)

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=2,  # Reduced for 6GB VRAM safety
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,  # Effective batch=16
    learning_rate=2e-4,  # Increased for better convergence
    bf16=True,
    save_steps=50,
    logging_steps=5,  # More frequent logging
    save_total_limit=2,
    warmup_steps=35,  # Optimized for 250 examples (~15% of total steps)
    optim="paged_adamw_8bit",
    report_to="none",
    dataloader_drop_last=True,
    group_by_length=True,  # Group similar length sequences for efficiency
    eval_strategy="epoch",  # Evaluate after each epoch
    save_strategy="epoch",  # Save after each epoch
    load_best_model_at_end=True,  # Load best checkpoint at end
    metric_for_best_model="eval_loss",  # Use eval loss to determine best model
    greater_is_better=False,  # Lower eval loss is better
)

# Custom data collator for padding with label masking
@dataclass
class DataCollatorForCompletionOnlyLM:
    tokenizer: AutoTokenizer
    pad_to_multiple_of: int = 8
    
    def __call__(self, features):
        # Extract sequences
        input_ids = [f["input_ids"] for f in features]
        labels = [f["labels"] for f in features]
        attention_mask = [f["attention_mask"] for f in features]
        
        # Find max length in batch
        max_length = max(len(ids) for ids in input_ids)
        # Pad to multiple of 8 for efficiency
        if self.pad_to_multiple_of:
            max_length = ((max_length + self.pad_to_multiple_of - 1) // 
                         self.pad_to_multiple_of * self.pad_to_multiple_of)
        
        # Pad all sequences
        padded_input_ids = []
        padded_labels = []
        padded_attention_mask = []
        
        for ids, labs, mask in zip(input_ids, labels, attention_mask):
            padding_length = max_length - len(ids)
            
            padded_input_ids.append(ids + [self.tokenizer.pad_token_id] * padding_length)
            padded_labels.append(labs + [-100] * padding_length)
            padded_attention_mask.append(mask + [0] * padding_length)
        
        return {
            "input_ids": torch.tensor(padded_input_ids, dtype=torch.long),
            "labels": torch.tensor(padded_labels, dtype=torch.long),
            "attention_mask": torch.tensor(padded_attention_mask, dtype=torch.long)
        }

# Use custom data collator
data_collator = DataCollatorForCompletionOnlyLM(
    tokenizer=tokenizer,
    pad_to_multiple_of=8
)

# Early stopping callback (stop if eval_loss doesn't improve)
early_stopping = EarlyStoppingCallback(
    early_stopping_patience=1,  # Stop if no improvement for 1 epoch
    early_stopping_threshold=0.001  # Minimum improvement threshold
)

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized,
    eval_dataset=eval_tokenized,
    data_collator=data_collator,
    callbacks=[early_stopping]  # Add early stopping
)

# Start fine-tuning
print("\n" + "="*50)
print("Starting fine-tuning...")
print("="*50 + "\n")

trainer.train()

# Get final evaluation metrics
print("\n" + "="*50)
print("Final Evaluation:")
print("="*50)
eval_results = trainer.evaluate()
print(f"Final Eval Loss: {eval_results['eval_loss']:.4f}")
print(f"Final Perplexity: {torch.exp(torch.tensor(eval_results['eval_loss'])):.2f}")

# Save the fine-tuned model
print("\nSaving fine-tuned model...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"\n✅ Fine-tuning complete! Model saved to: {OUTPUT_DIR}")
print("\nNext steps:")
print("1. Update rag_llama.py to load the fine-tuned model")
print("2. Test the conversational behavior")
print("3. Verify RAG still works for factual questions")
