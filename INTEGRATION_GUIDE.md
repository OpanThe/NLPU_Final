# AI Model Integration Guide

Complete guide for integrating Llama 3.2 and Gemini 2.5 Flash models with frontend and backend.

## 🏗️ Architecture Overview

```
Frontend (React/Vite)
      ↓
Backend (Node.js/Express)
      ↓
Python Backend (FastAPI)
      ↓
AI Models (Llama 3.2 via Ollama / Gemini 2.5 via API)
```

---

## 🚀 Quick Start

### 1. Start Python Backend (FastAPI)
```bash
# In root directory
python -m uvicorn main_backend:app --reload --port 8000
```

### 2. Start Node.js Backend
```bash
cd backend
npm install  # First time only
npm start
```

### 3. Start Frontend
```bash
cd frontend
npm install  # First time only
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:5173
- Node.js Backend: http://localhost:5000
- Python Backend: http://localhost:8000

---

## 📂 File Structure

```
NLP_FINAL/
├── backend/              # Node.js Backend
│   ├── server.js        # Express server with 2 models
│   ├── package.json
│   └── .env
├── frontend/            # React Frontend
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── ChatWindow.jsx
│   │       └── ModelSwitcher.jsx
│   └── package.json
├── main_backend.py      # Python FastAPI Backend
├── rag_chatbot/
│   ├── rag_gemini.py   # Gemini RAG implementation
│   └── rag_llama.py    # Llama RAG implementation
└── data/
    └── student_handbook.md  # Knowledge base
```

---

## 🔧 Backend Configuration

### Node.js Backend (server.js)

**Available Models:**
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

**Python Backend Integration:**
```javascript
// Calls Python FastAPI backend
async function generateAIResponse(message, model) {
  const response = await axios.post('http://localhost:8000/chat', {
    question: message,
    model_type: model  // 'llama' or 'gemini'
  });
  return response.data.answer;
}
```

### Python Backend (main_backend.py)

**Endpoints:**
- `POST /chat` - Send message to AI model
- Request body: `{ "question": "...", "model_type": "llama" }`
- Response: `{ "answer": "...", "source": "..." }`

**Model Routing:**
```python
if model == "gemini":
    answer = gemini_qa(question)
    source_used = "Gemini 2.5 Flash"
elif model == "llama":
    answer = llama_qa(question)
    source_used = "Llama 3.2 (Local)"
```

---

## 🌐 API Endpoints

### Node.js Backend (Port 5000)

#### Get Available Models
```http
GET /api/models
```
**Response:**
```json
{
  "success": true,
  "models": [
    {
      "id": "llama",
      "name": "Llama 3.2",
      "provider": "local",
      "description": "Local Ollama model - Fast & Private",
      "icon": "🦙"
    },
    {
      "id": "gemini",
      "name": "Gemini 2.5 Flash",
      "provider": "google",
      "description": "Cloud-based Google AI",
      "icon": "✨"
    }
  ]
}
```

#### Send Chat Message
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What is plagiarism?",
  "model": "llama",
  "sessionId": "session_123"
}
```

**Response:**
```json
{
  "success": true,
  "session": "session_123",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "What is plagiarism?",
      "timestamp": "2026-01-29T10:00:00Z",
      "model": "llama"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Plagiarism is...",
      "timestamp": "2026-01-29T10:00:02Z",
      "model": "llama"
    }
  ]
}
```

#### Get Chat History
```http
GET /api/chat-history/:sessionId
```

#### Clear Chat History
```http
DELETE /api/chat-history/:sessionId
```

### Python Backend (Port 8000)

#### Chat with AI
```http
POST /chat
Content-Type: application/json

{
  "question": "Can I do plagiarism?",
  "model_type": "gemini"
}
```

**Response:**
```json
{
  "answer": "NO. Plagiarism is STRICTLY PROHIBITED...",
  "source": "Gemini 2.5 Flash"
}
```

---

## 💻 Frontend Integration

### Using Fetch API
```javascript
// Get available models
const getModels = async () => {
  const response = await fetch('http://localhost:5000/api/models');
  const data = await response.json();
  return data.models;
};

// Send chat message
const sendMessage = async (message, model) => {
  const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      model,
      sessionId: 'session_123'
    })
  });
  
  const data = await response.json();
  return data;
};
```

### Using Axios
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// Get models
const getModels = async () => {
  const { data } = await axios.get(`${API_URL}/models`);
  return data.models;
};

// Send message
const sendMessage = async (message, model, sessionId) => {
  const { data } = await axios.post(`${API_URL}/chat`, {
    message,
    model,
    sessionId
  });
  return data;
};
```

### React Component Example
```jsx
import { useState, useEffect } from 'react';

function ChatWindow() {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('llama');
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Load available models on mount
    fetch('http://localhost:5000/api/models')
      .then(res => res.json())
      .then(data => {
        setModels(data.models);
      });
  }, []);

  const handleSend = async () => {
    if (!message.trim()) return;

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          model: selectedModel,
          sessionId: 'user_session'
        })
      });

      const data = await response.json();
      setMessages(data.messages);
      setMessage('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      {/* Model Selector */}
      <select 
        value={selectedModel} 
        onChange={(e) => setSelectedModel(e.target.value)}
      >
        {models.map(model => (
          <option key={model.id} value={model.id}>
            {model.icon} {model.name}
          </option>
        ))}
      </select>

      {/* Messages */}
      <div>
        {messages.map(msg => (
          <div key={msg.id}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
      </div>

      {/* Input */}
      <input 
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

---

## ⚙️ Environment Configuration

### backend/.env
```env
PORT=5000
PYTHON_BACKEND_URL=http://localhost:8000
```

### .env (root directory)
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🔄 Data Flow

### Sending a Message

1. **User types message** in frontend
2. **Frontend sends** to Node.js backend:
   ```
   POST http://localhost:5000/api/chat
   Body: { message: "What is GPA?", model: "llama" }
   ```

3. **Node.js backend** receives request and forwards to Python:
   ```
   POST http://localhost:8000/chat
   Body: { question: "What is GPA?", model_type: "llama" }
   ```

4. **Python FastAPI** processes request:
   - If model = "llama": calls `llama_qa()` 
   - If model = "gemini": calls `gemini_qa()`

5. **AI model** processes with RAG:
   - Retrieves relevant documents from FAISS
   - Generates contextualized answer
   - Returns response

6. **Python returns** to Node.js:
   ```json
   { "answer": "GPA is...", "source": "Llama 3.2" }
   ```

7. **Node.js returns** to Frontend:
   ```json
   {
     "success": true,
     "messages": [...],
     "history": [...]
   }
   ```

8. **Frontend displays** the AI response to user

---

## 🐛 Troubleshooting

### Python Backend Not Running
**Error:** "Cannot connect to AI backend"
**Solution:** Start Python backend first
```bash
uvicorn main_backend:app --reload --port 8000
```

### Ollama Not Running
**Error:** "Llama Error: Connection refused"
**Solution:** Start Ollama service
```bash
ollama serve
```

### Gemini API Error
**Error:** "Gemini Error: Invalid API key"
**Solution:** Check your `.env` file has valid `GEMINI_API_KEY`

### CORS Error
**Error:** "CORS policy blocked"
**Solution:** Ensure backend has CORS enabled:
```javascript
app.use(cors({
  origin: ['http://localhost:5173', 'http://localhost:5000'],
  credentials: true
}));
```

### Port Already in Use
**Error:** "Port 8000 already in use"
**Solution:** Kill the process or use different port
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

## 🧪 Testing the Integration

### Test Python Backend
```bash
# Test Llama model
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is GPA?", "model_type": "llama"}'

# Test Gemini model
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Can I gamble?", "model_type": "gemini"}'
```

### Test Node.js Backend
```bash
# Get models
curl http://localhost:5000/api/models

# Send message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is plagiarism?",
    "model": "llama",
    "sessionId": "test_session"
  }'
```

### Test from Browser Console
```javascript
// Test getting models
fetch('http://localhost:5000/api/models')
  .then(r => r.json())
  .then(console.log);

// Test sending message
fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Can I do plagiarism?',
    model: 'gemini',
    sessionId: 'test'
  })
})
  .then(r => r.json())
  .then(console.log);
```

---

## 📊 Performance Tips

### For Faster Response Times:
1. **Use Llama for quick queries** (local, no API delay)
2. **Use Gemini for complex questions** (more powerful)
3. **Keep Ollama running** in background
4. **Enable response caching** for common questions

### For Better Accuracy:
1. **Update student_handbook.md** with more information
2. **Increase chunk_size** in RAG settings (500 → 700)
3. **Adjust temperature** (lower = more focused)

---

## 🚀 Deployment Checklist

- [ ] Python backend runs on port 8000
- [ ] Node.js backend runs on port 5000
- [ ] Frontend runs on port 5173
- [ ] Ollama service is running
- [ ] Gemini API key is configured
- [ ] CORS is properly configured
- [ ] All dependencies are installed
- [ ] Environment variables are set

---

## 📚 Next Steps

1. **Customize UI**: Update frontend components in `frontend/src/components/`
2. **Add Features**: Implement conversation history, export chat, etc.
3. **Optimize Models**: Fine-tune responses, adjust RAG parameters
4. **Add Authentication**: Secure the API endpoints
5. **Deploy**: Deploy to cloud services (Vercel, Railway, etc.)

---

**Need Help?** Check the error messages and refer to the Troubleshooting section above.
