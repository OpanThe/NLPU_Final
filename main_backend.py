from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import os
import re
import random

# Import your modules
# Ensure rag_gemini is importable. If you run this from the root folder, this works.
from rag_chatbot.rag_gemini import rag_qa as gemini_qa
from rag_chatbot.rag_llama import rag_llama_qa as llama_qa
from rag_chatbot.rag_qwen import rag_qwen_qa as qwen_qa
from database_config import ChatDatabase

app = FastAPI(title="Academic RAG Backend")

# Initialize database connection
db = ChatDatabase(
    host="localhost",
    user="root",
    password="",  # Change this if you set a password in phpMyAdmin
    database="jarvis_chatbot"
)

# Connect to database on startup
@app.on_event("startup")
async def startup_event():
    try:
        db.connect()
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("⚠️  Chat history will not be saved!")
        # Don't crash - let app run without database

# Disconnect from database on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    db.disconnect()

# ============================
# CORS (Important for Frontend)
# ============================
# This allows your friend's frontend (running on a different port) to talk to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Data Models
# ============================
class ChatRequest(BaseModel):
    question: str
    model_type: str = "llama"  # Options: "gemini", "llama", or "qwen"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    source: str

class GreetingResponse(BaseModel):
    greeting: str
    suggested_questions: list[str]
    source: str

class SessionData(BaseModel):
    session_id: str
    model_type: str
    title: Optional[str] = None

class MessageData(BaseModel):
    role: str
    content: str
    model_type: Optional[str] = None
    timestamp: Optional[str] = None

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
    
    if model == "gemini":
        source_used = "Gemini 2.5 Flash"
    elif model == "qwen":
        source_used = "Qwen 2.5 3B (Fine-tuned)"
    else:
        source_used = "Llama 3.2 3B (Fine-tuned)"
    
    return GreetingResponse(
        greeting=greeting,
        suggested_questions=suggested_questions,
        source=source_used
    )

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    question = request.question
    model = request.model_type.lower()
    session_id = request.session_id
    
    # Create session if not exists
    if session_id:
        db.create_session(session_id, model)
        
        # Save user message to database
        db.save_message(session_id, "user", question)
    
    answer = ""
    source_used = ""

    # GEMINI MODEL
    if model == "gemini":
        try:
            answer = gemini_qa(question)
            source_used = "Gemini 2.5 Flash"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini Error: {str(e)}")

    # LLAMA 3.2 MODEL (Fine-tuned)
    elif model == "llama":
        try:
            answer = llama_qa(question)
            source_used = "Llama 3.2 3B (Fine-tuned)"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Llama Error: {str(e)}")

    # QWEN 2.5 MODEL (Fine-tuned)
    elif model == "qwen":
        try:
            answer = qwen_qa(question)
            source_used = "Qwen 2.5 3B (Fine-tuned)"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Qwen Error: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Invalid model_type. Use 'gemini', 'llama', or 'qwen'.")

    # Save assistant response to database
    if session_id:
        db.save_message(session_id, "assistant", answer, model_type=model)

    return ChatResponse(answer=answer, source=source_used)

# ============================
# History/Session Management Routes
# ============================
@app.get("/sessions")
def get_sessions():
    """Get all chat sessions with preview"""
    try:
        sessions = db.get_all_sessions(limit=50)
        return {"success": True, "sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@app.get("/session/{session_id}/messages")
def get_session_messages(session_id: str):
    """Get all messages from a specific session"""
    try:
        messages = db.get_session_messages(session_id)
        return {"success": True, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    """Delete a chat session"""
    try:
        success = db.delete_session(session_id)
        if success:
            return {"success": True, "message": "Session deleted"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@app.put("/session/{session_id}/title")
def update_session_title(session_id: str, title: str):
    """Update session title"""
    try:
        success = db.update_session_title(session_id, title)
        if success:
            return {"success": True, "message": "Title updated"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update title")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

# Run with: uvicorn main_backend:app --reload