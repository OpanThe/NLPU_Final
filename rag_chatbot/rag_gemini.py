import os
from dotenv import load_dotenv
from typing import List, Dict
 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

import google.generativeai as genai

# =========================
# ENV & GEMINI
# =========================
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"

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
# VECTOR STORE (Enhanced)
# =========================
def build_vectorstore():
    documents = load_documents()

    # Improved chunking - same as chatbot.py
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # Increased from 300
        chunk_overlap=200    # Increased from 50
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    return FAISS.from_documents(chunks, embeddings)

print("🔄 Building vector store for Gemini...")
vectorstore = build_vectorstore()
print("✅ Vector store ready.")

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
# RAG FUNCTION (Enhanced with Jarvis AI)
# =========================
def rag_qa(question: str) -> str:
    """Enhanced RAG with conversation context and Jarvis AI personality"""
    
    # Use MMR for better diversity - same as chatbot.py
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,              # Retrieve 5 documents
            "fetch_k": 12,       # Fetch candidates
            "lambda_mult": 0.75  # Relevance weight
        }
    )
    
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        return "I don't have that information in the provided documents. Please contact the university administration."

    # Format context - remove document numbering to avoid AI mentioning "Document 1", etc.
    context = "\n\n---\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )
    
    # Get conversation history
    chat_history = format_chat_history()

    # Optimized RAG prompt
    prompt = f"""You are Jarvis AI, a helpful assistant for President University students.

Context:
{context}

Recent Conversation:
{chat_history}

User Input: {question}

RULES:
- If user says ONLY "hi", "hello", "hey" (nothing else): Say "Hello! I'm Jarvis AI, here to help with President University information. How can I assist you today?"
- If user says ONLY "thank you", "thanks" (nothing else): Say "You're welcome! Happy to help!"
- For ANY OTHER INPUT (questions, requests): Answer directly from Context. DO NOT add greetings like "Hello" or "I'm Jarvis AI". Just answer the question.
- Use numbered lists for steps, bullet points for options
- Never mention "document", "context", or "handbook"
- If answer not in Context, say you don't have that information

Answer:"""

    # Configure Gemini with temperature control
    generation_config = genai.GenerationConfig(
        temperature=0.05,        # Low temperature for accuracy
        top_p=0.9,
        max_output_tokens=1024,
    )
    
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config=generation_config
    )
    
    response = model.generate_content(prompt)
    answer = response.text
    
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
    """Alias for compatibility with main.py"""
    return rag_qa(pertanyaan)

