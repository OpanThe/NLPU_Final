# NLP_FINAL/rag_chatbot/rag_qwen.py
# Qwen 2.5 3B RAG implementation using Fine-Tuned Model
import os
import torch
from typing import List, Dict

# Set HuggingFace to work offline
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)
from peft import PeftModel

# =========================
# CONFIGURATION
# =========================
BASE_MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
FINETUNED_MODEL_PATH = "./models/jarvis-qwen-finetuned"

# Conversation history storage
conversation_history: List[Dict[str, str]] = []

# =========================
# LOAD DOCUMENTS
# =========================
def load_documents():
    docs = []
    data_dir = "data"

    for file in os.listdir(data_dir):
        if file.endswith(".md"):
            path = os.path.join(data_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                docs.append(
                    Document(
                        page_content=content,
                        metadata={"source": file}
                    )
                )
    return docs

# =========================
# VECTOR STORE
# =========================
def build_vectorstore():
    documents = load_documents()

    # Markdown-aware chunking: splits by headers (preserves structure)
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]
    
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False  # Keep headers for context
    )
    
    # First pass: split by markdown structure
    md_chunks = []
    for doc in documents:
        splits = markdown_splitter.split_text(doc.page_content)
        for split in splits:
            # Preserve metadata and add header info
            split.metadata.update(doc.metadata)
            md_chunks.append(split)
    
    # Second pass: split large sections (tables, long paragraphs)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Increased from 800 for better context coverage
        chunk_overlap=250,  # Increased overlap to capture more information
        separators=["\n\n", "\n", "|", " ", ""]  # Table-aware
    )
    
    final_chunks = text_splitter.split_documents(md_chunks)

    # Embeddings - USE GPU for 10x faster performance!
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': device},
        encode_kwargs={'normalize_embeddings': True},
        cache_folder=os.path.join(os.path.expanduser("~"), ".cache", "huggingface")
    )
    print(f"🚀 Embeddings using: {device.upper()}")

    return FAISS.from_documents(final_chunks, embeddings)

print("🔄 Building vector store for Qwen...")
vectorstore = build_vectorstore()
print("✅ Vector store ready.")

# =========================
# LOAD FINE-TUNED MODEL
# =========================
print("🔄 Loading fine-tuned Jarvis AI (Qwen) model...")

# Quantization config for inference (saves memory)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load base model
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# Load fine-tuned LoRA adapters
model = PeftModel.from_pretrained(base_model, FINETUNED_MODEL_PATH)
print("✅ Fine-tuned Qwen model loaded successfully!")

print("✅ Jarvis AI (Qwen) ready for questions!")

# Generation config - Balanced speed and accuracy
generation_config = {
    "max_new_tokens": 512,  # Full response length
    "temperature": 0.2,
    "top_p": 0.85,
    "top_k": 40,
    "repetition_penalty": 1.15,
    "do_sample": True,
    "pad_token_id": tokenizer.eos_token_id
}

# =========================
# HELPER FUNCTIONS
# =========================
def format_chat_history() -> str:
    """Format recent conversation history"""
    if not conversation_history:
        return "(No previous conversation)"
    
    formatted = ""
    for exchange in conversation_history[-2:]:  # Last 2 exchanges
        formatted += f"User asked: {exchange['question']}\n"
        formatted += f"You (Jarvis) answered: {exchange['answer']}\n\n"
    return formatted.strip()

def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    print("🗑️ Conversation history cleared")

# =========================
# RAG FUNCTION
# =========================
def rag_qwen_qa(question: str) -> str:
    """Enhanced RAG with conversation context and Jarvis AI personality (Qwen 2.5)"""
    
    # Detect if this is a simple greeting or thanks (no context needed)
    question_lower = question.lower().strip()
    is_greeting = any(greet in question_lower for greet in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]) and len(question_lower.split()) <= 3
    is_thanks = "thank" in question_lower or "thanks" in question_lower or "thx" in question_lower or "appreciate" in question_lower
    is_identity = "who are you" in question_lower or "what is your name" in question_lower or "your name" in question_lower or "what can you help" in question_lower or "what do you do" in question_lower or "what can you do" in question_lower
    
    # For simple greetings/thanks, skip RAG and respond directly
    if is_greeting or is_thanks or is_identity:
        prompt_text = f"""<|im_start|>system
You are Jarvis AI, a formal but friendly assistant for President University.<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
"""
        inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, **generation_config)
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=False)
        
        # Extract assistant response
        if "<|im_start|>assistant\n" in full_response:
            answer = full_response.split("<|im_start|>assistant\n")[-1]
            answer = answer.split("<|im_end|>")[0].strip()
        else:
            answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        
        conversation_history.append({"question": question, "answer": answer})
        if len(conversation_history) > 3:
            conversation_history[:] = conversation_history[-3:]
        return answer
    
    # For factual questions, use RAG (optimized for speed)
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 3,  # Reduced from 5 - fewer docs = faster
            "fetch_k": 8,  # Reduced from 20 for faster search
            "lambda_mult": 0.5  # More diversity (less redundancy)
        }
    )
    
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        return "I don't have that information in the provided documents. Please contact the university administration."

    # Filter for relevance: remove very short or uninformative chunks
    filtered_docs = [
        doc for doc in retrieved_docs
        if len(doc.page_content.strip()) > 100  # Stricter minimum length
    ]
    
    if not filtered_docs:
        return "I couldn't find relevant information in the documents. Please contact the relevant department."

    # Format context with source attribution
    context_parts = []
    for i, doc in enumerate(filtered_docs, 1):
        source = doc.metadata.get('source', 'Unknown')
        context_parts.append(f"[Source {i}: {source}]\n{doc.page_content}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Get conversation history
    chat_history = format_chat_history()

    # Simplified RAG prompt (Qwen format)
    prompt_text = f"""<|im_start|>system
You are Jarvis AI, a helpful assistant for President University. Answer questions using ONLY the provided context. If information is not in the context, say you don't have it.<|im_end|>
<|im_start|>user
CONTEXT:
{context}

PREVIOUS CONVERSATION:
{chat_history}

QUESTION: {question}

INSTRUCTIONS:
1. Answer using ONLY the context above - do NOT use general knowledge
2. Start directly with the answer - do NOT repeat the question
3. If the question is about another university (Harvard, Stanford, etc.), say: "I only have information about President University."
4. If the question is unclear, ask for clarification
5. If information is missing from context, say: "Sorry, I don't have any information about that."
6. Keep your answers natural and conversational - avoid repeating the same phrases
7. Include specific numbers, dates, and requirements from the context

Answer:<|im_end|>
<|im_start|>assistant
"""
    
    # Tokenize and generate
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, **generation_config)
    
    # Decode full response
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    
    # Extract only the assistant's response
    if "<|im_start|>assistant\n" in full_response:
        answer = full_response.split("<|im_start|>assistant\n")[-1]
        answer = answer.split("<|im_end|>")[0].strip()
    else:
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
    # Add to conversation history
    conversation_history.append({
        "question": question,
        "answer": answer
    })
    
    # Keep only last 3 exchanges
    if len(conversation_history) > 3:
        conversation_history[:] = conversation_history[-3:]
    
    return answer


# =========================
# ALIAS FOR COMPATIBILITY
# =========================
def tanya(pertanyaan: str) -> str:
    """Alias for compatibility"""
    return rag_qwen_qa(pertanyaan)
