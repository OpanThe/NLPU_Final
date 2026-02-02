# 🎓 President University RAG Chatbot

An intelligent chatbot system for President University using Retrieval-Augmented Generation (RAG) with multiple implementation options.

## 📁 Project Structure

```
NLP_FINAL/
├── data/                          # Knowledge base documents
│   ├── faq.md                    # Frequently Asked Questions
│   └── student_handbook.md       # Student Handbook
│
├── rag_chatbot/                   # RAG implementation modules
│   ├── __init__.py               # Package initialization
│   ├── rag_gemini.py             # Gemini-based RAG (Cloud API)
│   ├── rag_llama.py              # Local Llama-based RAG (Placeholder)
│   └── rules.py                  # Rule-based responses
│
├── chatbot.py                     # Full-featured RAG with Ollama/Llama
├── main.py                        # Simple CLI interface (Gemini)
├── main_backend.py                # FastAPI REST API backend
├── test_gemini.py                 # Test script for Gemini
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment (if not already exists)
python -m venv nlp_env

# Activate virtual environment
# Windows:
nlp_env\Scripts\activate
# Unix/MacOS:
source nlp_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your Gemini API key
# Get API key from: https://makersuite.google.com/app/apikey
```

### 3. Choose Your Implementation

## 📋 Implementation Options

### Option 1: Simple Gemini CLI (`main.py`)
**Best for:** Quick testing with Gemini API

```bash
python main.py
```

**Features:**
- ✅ Simple command-line interface
- ✅ Uses Gemini Cloud API
- ✅ No local setup required
- ❌ No evaluation metrics

---

### Option 2: FastAPI Backend (`main_backend.py`)
**Best for:** Production deployment with frontend integration

```bash
# Start the server
uvicorn main_backend:app --reload

# Or with specific port
uvicorn main_backend:app --reload --port 8000
```

**API Endpoints:**
- `GET /` - Health check
- `POST /chat` - Chat endpoint

**Request Example:**
```json
{
  "question": "What are the admission requirements?",
  "model_type": "hybrid"
}
```

**Model Types:**
- `gemini` - Use Gemini Cloud API only
- `llama` - Use local Llama (placeholder)
- `hybrid` - Check rules first, fallback to Gemini

**Features:**
- ✅ REST API for frontend integration
- ✅ CORS enabled
- ✅ Hybrid approach (rules + RAG)
- ✅ Multiple model support
- ❌ No conversation memory
- ❌ No evaluation metrics

---

### Option 3: Full-Featured RAG (`chatbot.py`)
**Best for:** Advanced use with evaluation and metrics

**Prerequisites:**
- Install and run Ollama: https://ollama.ai
- Pull Llama model: `ollama pull llama3.2`
- Start Ollama: `ollama serve`

```bash
python chatbot.py
```

**Features:**
- ✅ Advanced RAG implementation
- ✅ Conversation memory (5 messages)
- ✅ Evaluation metrics (precision, adherence)
- ✅ Custom document chunking
- ✅ In-memory vector store
- ✅ ROUGE scores & evaluation reports
- ❌ Requires local Ollama setup

**Commands:**
- Type your question to chat
- `clear` - Clear conversation history
- `eval` - Show evaluation summary
- `save` - Save evaluation report to CSV
- `quit` - Exit chatbot

---

## 📦 Dependencies

### Core Libraries
- `langchain` & `langchain-community` - RAG framework
- `faiss-cpu` - Vector similarity search
- `sentence-transformers` - Text embeddings
- `google-generativeai` - Gemini API
- `python-dotenv` - Environment variables

### API & Web
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `requests` - HTTP client

### ML & Evaluation
- `numpy` - Numerical operations
- `scikit-learn` - ML utilities
- `pandas` - Data manipulation
- `rouge-score` - Text evaluation

## 🔧 Configuration

### Gemini API Setup
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Ollama Setup (for chatbot.py)
1. Install from [ollama.ai](https://ollama.ai)
2. Run: `ollama pull llama3.2`
3. Start server: `ollama serve`

### Document Management
- Add knowledge base documents to `data/` folder
- Supported format: Markdown (.md)
- Files are automatically loaded by RAG system

## 🎯 Use Cases

| Use Case | Recommended Implementation |
|----------|---------------------------|
| Quick testing | `main.py` |
| Production API | `main_backend.py` |
| Research & evaluation | `chatbot.py` |
| Frontend integration | `main_backend.py` |
| Offline/local only | `chatbot.py` |

## 🧪 Testing

```bash
# Test Gemini connection
python test_gemini.py

# Test FastAPI backend
curl http://localhost:8000/

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the tuition fee?", "model_type": "gemini"}'
```

## 📊 Evaluation Metrics (chatbot.py only)

The full-featured chatbot tracks:
- **Retrieval Precision**: Relevance of retrieved documents
- **Context Adherence**: How well answers stick to context
- **ROUGE Scores**: Text similarity metrics
- **Response Statistics**: Length, sources, timing

Export evaluation report:
```python
# In chatbot, type: save
# Creates: evaluation_report.csv
```

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- Use `.env.example` as template only
- In production, restrict CORS in `main_backend.py`:
  ```python
  allow_origins=["https://your-frontend-domain.com"]
  ```

## 🐛 Troubleshooting

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Gemini API Errors
- Check API key in `.env`
- Verify internet connection
- Check API quota at [Google AI Studio](https://makersuite.google.com)

### Ollama Connection Errors
```bash
# Check if Ollama is running
curl http://localhost:11434

# Start Ollama
ollama serve

# Verify model is installed
ollama list
```

### Module Not Found Errors
```bash
# Ensure virtual environment is activated
# Windows:
nlp_env\Scripts\activate

# Reinstall package
pip install -e .
```

## 📝 Development Notes

### Adding New Documents
1. Place `.md` files in `data/` folder
2. Restart the application
3. Documents are automatically loaded

### Extending Rule-Based Responses
Edit `rag_chatbot/rules.py`:
```python
RULES = {
    "your keyword": "Your response",
    # Add more rules...
}
```

### Custom Model Configuration
Edit model parameters in respective files:
- Gemini: `rag_chatbot/rag_gemini.py` (MODEL_NAME)
- Llama: `chatbot.py` (LLMConfig)

## 👥 Contributors

President University NLP Final Project Team

## 📄 License

Academic Project - President University

---

**Questions or Issues?** Contact the Academic Bureau or your project supervisor.
