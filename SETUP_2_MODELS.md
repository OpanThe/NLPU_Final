# Quick Setup - 2 AI Models Integration

## 🎯 What Changed

**BEFORE:** 5 AI models (GPT-4, GPT-3.5, Claude Opus, Claude Sonnet, Gemini Pro)
**AFTER:** 2 AI models (Llama 3.2, Gemini 2.5 Flash)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Python Backend
```bash
# Activate virtual environment first
nlp_env\Scripts\activate

# Start FastAPI
python -m uvicorn main_backend:app --reload --port 8000
```

### Step 2: Start Node.js Backend
```bash
cd backend
npm start
```

### Step 3: Start Frontend
```bash
cd frontend
npm run dev
```

### OR Use the Script:
```bash
start_all.bat
```

---

## 📡 API Changes

### Node.js Backend (server.js)

**OLD Models Array:**
```javascript
// 5 models: GPT-4, GPT-3.5, Claude 3 Opus, Claude 3 Sonnet, Gemini Pro
```

**NEW Models Array:**
```javascript
const AVAILABLE_MODELS = [
  {
    id: 'llama',
    name: 'Llama 3.2',
    provider: 'local',
    description: 'Local Ollama model - Fast & Private',
    icon: '🦙'
  },
  {
    id: 'gemini',
    name: 'Gemini 2.5 Flash',
    provider: 'google',
    description: 'Cloud-based Google AI',
    icon: '✨'
  }
];
```

**Integration with Python:**
```javascript
// Now calls Python backend instead of mock responses
async function generateAIResponse(message, model) {
  const response = await axios.post('http://localhost:8000/chat', {
    question: message,
    model_type: model
  });
  return response.data.answer;
}
```

### Python Backend (main_backend.py)

**OLD:**
```python
model_type: str = "hybrid"  # Options: "gemini", "llama", "hybrid"
```

**NEW:**
```python
model_type: str = "llama"  # Options: "gemini" or "llama"
```

**Route Handler:**
```python
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    if model == "gemini":
        answer = gemini_qa(question)
        source = "Gemini 2.5 Flash"
    elif model == "llama":
        answer = llama_qa(question)
        source = "Llama 3.2 (Local)"
    return ChatResponse(answer=answer, source=source)
```

---

## 🔄 Data Flow

```
User Input (Frontend)
        ↓
[POST] /api/chat → Node.js Backend (Port 5000)
        ↓
[POST] /chat → Python Backend (Port 8000)
        ↓
    Llama 3.2 OR Gemini 2.5
        ↓
    RAG Processing (FAISS + Documents)
        ↓
Response → Python → Node.js → Frontend
```

---

## 🧪 Test the Integration

### 1. Test Python Backend Directly
```bash
# Test Llama
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Can I gamble?\", \"model_type\": \"llama\"}"

# Test Gemini
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is GPA?\", \"model_type\": \"gemini\"}"
```

### 2. Test Node.js Backend
```bash
# Get available models
curl http://localhost:5000/api/models

# Send message with Llama
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Can I do plagiarism?\", \"model\": \"llama\"}"
```

### 3. Test from Browser Console
```javascript
// Get models
fetch('http://localhost:5000/api/models').then(r => r.json()).then(console.log);

// Send message
fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'What is plagiarism?',
    model: 'llama',
    sessionId: 'test'
  })
}).then(r => r.json()).then(console.log);
```

---

## 📱 Frontend Usage

### Model Selection
```jsx
// User can select between 2 models
<select onChange={(e) => setModel(e.target.value)}>
  <option value="llama">🦙 Llama 3.2 (Fast, Local)</option>
  <option value="gemini">✨ Gemini 2.5 (Cloud, Powerful)</option>
</select>
```

### Send Message
```javascript
const sendMessage = async (message, model) => {
  const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, model, sessionId: 'user_123' })
  });
  return response.json();
};
```

---

## ⚙️ Configuration Files

### backend/.env
```env
PORT=5000
PYTHON_BACKEND_URL=http://localhost:8000
```

### Root .env
```env
GEMINI_API_KEY=your_api_key_here
```

---

## 🐛 Common Issues

### Issue 1: "Cannot connect to AI backend"
**Cause:** Python backend not running
**Fix:** Start Python backend first
```bash
python -m uvicorn main_backend:app --reload --port 8000
```

### Issue 2: "Llama Error: Connection refused"
**Cause:** Ollama not running
**Fix:** Start Ollama
```bash
ollama serve
```

### Issue 3: Frontend can't reach backend
**Cause:** CORS issue or wrong URL
**Fix:** Check CORS in server.js
```javascript
app.use(cors());  // Should be enabled
```

---

## 📊 Model Comparison

| Feature | Llama 3.2 | Gemini 2.5 Flash |
|---------|-----------|------------------|
| Speed | ⚡ Fast | 🐢 Slower (API) |
| Privacy | 🔒 Local | ☁️ Cloud |
| Cost | 💰 Free | 💸 API costs |
| Power | 🧠 Good | 🚀 Excellent |
| Internet | ❌ Not needed | ✅ Required |

**Recommendation:**
- Use **Llama 3.2** for quick queries and privacy
- Use **Gemini 2.5** for complex questions needing deeper understanding

---

## 📝 Files Modified

✅ `backend/server.js` - Reduced to 2 models, integrated with Python
✅ `main_backend.py` - Removed hybrid mode, clean 2-model routing
✅ Created `INTEGRATION_GUIDE.md` - Complete documentation
✅ Created `start_all.bat` - Easy startup script
✅ Created `SETUP_2_MODELS.md` - This quick reference

---

## 🎯 Next Steps

1. ✅ Backend configured with 2 models
2. ✅ Python integration working
3. ⏳ Update frontend UI to show 2 models
4. ⏳ Test end-to-end flow
5. ⏳ Add model switching in chat interface

---

**Questions?** Check `INTEGRATION_GUIDE.md` for detailed documentation!
