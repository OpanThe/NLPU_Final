from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import re
import random

# Import your modules
# Ensure rag_gemini is importable. If you run this from the root folder, this works.
from rag_chatbot.rag_gemini import rag_qa as gemini_qa
from rag_chatbot.rag_llama import rag_llama_qa as llama_qa

app = FastAPI(title="Academic RAG Backend")

# ============================
# CORS (Important for Frontend)
# ============================
# This allows your friend's frontend (running on a different port) to talk to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Data Models
# ============================
class ChatRequest(BaseModel):
    question: str
    model_type: str = "llama"  # Options: "gemini" or "llama"

class ChatResponse(BaseModel):
    answer: str
    source: str

class GreetingResponse(BaseModel):
    greeting: str
    suggested_questions: list[str]
    source: str

# ============================
# Helper Functions
# ============================
def extract_questions_from_faq():
    """Extract all questions from FAQ markdown file"""
    faq_path = os.path.join("data", "faq.md")
    questions = []
    
    try:
        with open(faq_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Find all lines that start with ### (questions in the FAQ)
        question_pattern = r'^###\s+(.+)$'
        matches = re.findall(question_pattern, content, re.MULTILINE)
        questions = [q.strip() for q in matches if q.strip() and '?' in q]
        
    except Exception as e:
        print(f"Error reading FAQ: {e}")
        # Fallback questions if file reading fails
        questions = [
            "What are the graduation requirements?",
            "How do I apply for a scholarship?",
            "What is the code of ethics at President University?",
            "How can I contact the academic office?",
            "Can I drop the subjects or classes that I have been enrolled in?",
            "Can I change my concentration?",
            "What if I missed the deadline for enrollment?",
            "Why can't I access my GPA?"
        ]
    
    return questions

# ============================
# Routes
# ============================
@app.get("/")
def read_root():
    return {"status": "running", "message": "Academic RAG Backend is ready."}

@app.get("/greeting", response_model=GreetingResponse)
def greeting_endpoint(model_type: str = "llama"):
    """Generate initial greeting with 4 randomly selected questions from FAQ"""
    model = model_type.lower()
    
    # Get all questions from FAQ
    all_questions = extract_questions_from_faq()
    
    # Randomly select 4 questions
    if len(all_questions) >= 4:
        suggested_questions = random.sample(all_questions, 4)
    else:
        suggested_questions = all_questions
    
    greeting = "Hello! I'm Jarvis AI, your friendly assistant for President University! 😊\n\nI can help you with information about the university. Here are some questions you might want to ask:"
    
    source_used = "Gemini 2.5 Flash" if model == "gemini" else "Llama 3.2 (Local)"
    
    return GreetingResponse(
        greeting=greeting,
        suggested_questions=suggested_questions,
        source=source_used
    )

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    question = request.question
    model = request.model_type.lower()
    
    answer = ""
    source_used = ""

    # GEMINI MODEL
    if model == "gemini":
        try:
            answer = gemini_qa(question)
            source_used = "Gemini 2.5 Flash"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini Error: {str(e)}")

    # LLAMA 3.2 MODEL (Local Ollama)
    elif model == "llama":
        try:
            answer = llama_qa(question)
            source_used = "Llama 3.2 (Local)"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Llama Error: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Invalid model_type. Use 'gemini' or 'llama'.")

    return ChatResponse(answer=answer, source=source_used)

# Run with: uvicorn main_backend:app --reload