# NLP_FINAL/rag_chatbot/rag_llama.py
# Local LLaMA 3.2 RAG implementation using Ollama
import os
from typing import List, Dict

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# =========================
# CONFIGURATION
# =========================
MODEL_NAME = "llama3.2"

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

    # Improved chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    return FAISS.from_documents(chunks, embeddings)

print("🔄 Building vector store for Llama...")
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
# RAG FUNCTION
# =========================
def rag_llama_qa(question: str) -> str:
    """Enhanced RAG with conversation context and Jarvis AI personality"""
    
    # Use MMR for better diversity
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 12,
            "lambda_mult": 0.75
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
    prompt_template = """You are Jarvis AI, a helpful assistant for President University students.

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

    # Create prompt
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Initialize Ollama LLM
    llm = OllamaLLM(
        model=MODEL_NAME,
        temperature=0.05
    )
    
    # Create chain
    chain = prompt | llm | StrOutputParser()
    
    # Generate answer
    answer = chain.invoke({
        "context": context,
        "question": question,
        "chat_history": chat_history
    })
    
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
    return rag_llama_qa(pertanyaan)
