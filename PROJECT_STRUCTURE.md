# 📋 Project Structure & Files Explanation

## 📁 Directory Tree

```
chatbot-app/
│
├── 📂 backend/                           # Express.js Server
│   ├── server.js                         # Main application file
│   ├── package.json                      # Dependencies & scripts
│   ├── .env.example                      # Environment variables template
│   └── .gitignore                        # Git ignore rules
│
├── 📂 frontend/                          # React Frontend Application
│   ├── 📂 public/                        # Static assets
│   ├── 📂 src/                           # Source code
│   │   ├── 📂 components/                # React components
│   │   │   ├── ChatWindow.jsx           # Main chat container
│   │   │   ├── ChatMessage.jsx          # Message display component
│   │   │   ├── ChatInput.jsx            # Input form component
│   │   │   └── ModelSwitcher.jsx        # Model selection component
│   │   ├── 📂 utils/                    # Utility functions
│   │   │   └── api.js                   # API client service
│   │   ├── App.jsx                      # Main React component
│   │   ├── main.jsx                     # React entry point
│   │   └── index.css                    # Global styles & Tailwind
│   ├── index.html                       # HTML template
│   ├── vite.config.js                   # Vite bundler config
│   ├── tailwind.config.js               # Tailwind CSS config
│   ├── postcss.config.js                # PostCSS config
│   ├── package.json                     # Dependencies & scripts
│   └── .gitignore                       # Git ignore rules
│
├── README.md                            # Main documentation
├── SETUP_GUIDE.md                       # Installation guide
├── DEVELOPMENT_GUIDE.md                 # Development guide
├── AI_INTEGRATION_EXAMPLES.js           # Example AI API integrations
└── PROJECT_STRUCTURE.md                 # This file
```

## 📄 Files Explanation

### Backend Files

#### `backend/server.js`

**Purpose:** Main Express server file  
**Key Functions:**

- Initialize Express app with middleware (CORS, JSON parser)
- Define API routes for chat functionality
- Manage in-memory chat history storage
- Handle request/response for AI interactions

**Routes:**

- `GET /api/health` - Server health check
- `GET /api/models` - Get available AI models
- `POST /api/chat` - Send message and get response
- `GET /api/chat-history/:sessionId` - Retrieve chat history
- `DELETE /api/chat-history/:sessionId` - Clear chat history
- `GET /api/sessions` - Get all active sessions

**Key Variables:**

```javascript
chatHistory; // Object untuk store all conversations
messageId; // Counter untuk unique message IDs
AVAILABLE_MODELS; // Array dari supported AI models
```

#### `backend/package.json`

**Purpose:** Project configuration dan dependency list  
**Contains:**

- Project name, version, description
- Scripts untuk `npm start` dan `npm run dev`
- Dependencies: express, cors, dotenv, axios
- DevDependencies: nodemon untuk auto-reload

#### `backend/.env.example`

**Purpose:** Template untuk environment variables  
**Variables:**

```
PORT=5000
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
NODE_ENV=development
```

**How to Use:**

1. Copy file ini: `cp .env.example .env`
2. Edit `.env` dengan actual API keys
3. Server akan load variables dari `.env`

#### `backend/.gitignore`

**Purpose:** Tell Git yang files tidak perlu di-commit  
**Ignores:**

- node_modules/
- .env (sensitive data)
- .env.local
- \*.log files

---

### Frontend Files

#### `frontend/src/components/ChatWindow.jsx`

**Purpose:** Main container component untuk chat application  
**Features:**

- State management (messages, input, models, loading)
- Load available models on mount
- Handle sending messages
- Auto-scroll ke latest message
- Clear chat history function
- Model switching capability

**Key Hooks:**

```javascript
useState(messages); // Store all messages
useState(selectedModel); // Current selected model
useState(isLoading); // Loading state untuk API call
useEffect(); // Load models, auto-scroll
useRef(messagesEndRef); // Reference untuk scroll-to-bottom
```

**Functions:**

- `loadModels()` - Fetch available models dari backend
- `handleSendMessage()` - Send message dan get AI response
- `handleClearChat()` - Clear conversation history
- `handleModelChange()` - Switch AI model

#### `frontend/src/components/ChatMessage.jsx`

**Purpose:** Component untuk display individual messages  
**Props:**

- `message` - Message object dengan content, timestamp, model
- `isUser` - Boolean untuk determine styling (user vs assistant)

**Features:**

- Format timestamp
- Display model name badge
- Different styling untuk user vs assistant messages
- Message animation

#### `frontend/src/components/ChatInput.jsx`

**Purpose:** Input form component untuk new messages  
**Props:**

- `value` - Current input value
- `onChange` - Handler untuk input changes
- `onSend` - Handler untuk send action
- `isLoading` - Disable input saat loading

**Features:**

- Textarea dengan Shift+Enter untuk newline
- Send button dengan loading indicator
- Disabled state saat loading atau empty input
- Character counter (optional)

#### `frontend/src/components/ModelSwitcher.jsx`

**Purpose:** Dropdown untuk select AI model  
**Props:**

- `models` - Array dari available models
- `selectedModel` - Currently selected model
- `onModelChange` - Callback function saat model berubah
- `isLoading` - Disable dropdown saat loading

**Features:**

- Display semua available models
- Show model icon, name, dan description
- Current selection indicator
- Disabled state saat loading

#### `frontend/src/utils/api.js`

**Purpose:** API client service untuk backend communication  
**Features:**

- Axios instance dengan base URL
- API methods untuk semua endpoints
- Error handling
- Request/response interceptors (optional)

**Methods:**

```javascript
chatAPI.getModels(); // GET /api/models
chatAPI.sendMessage(); // POST /api/chat
chatAPI.getChatHistory(); // GET /api/chat-history/:sessionId
chatAPI.clearHistory(); // DELETE /api/chat-history/:sessionId
chatAPI.getSessions(); // GET /api/sessions
chatAPI.healthCheck(); // GET /api/health
```

#### `frontend/src/App.jsx`

**Purpose:** Root React component  
**Features:**

- Import CSS
- Render ChatWindow component
- Setup basic layout

#### `frontend/src/main.jsx`

**Purpose:** React entry point  
**Features:**

- Mount React app ke #root element
- Strict mode untuk development warnings
- Import App component dan CSS

#### `frontend/src/index.css`

**Purpose:** Global styles dan Tailwind CSS configuration  
**Contains:**

- Tailwind directives (@tailwind base, components, utilities)
- Global HTML/body styles
- Custom CSS classes untuk messages
- Animation keyframes
- Scrollbar styling
- Custom utility classes

**Custom Classes:**

```css
.message          - Message container styling
.message.user     - User message styling
.message.assistant - Assistant message styling
.message-enter    - Message animation
.model-badge      - Model indicator badge
.typing-indicator - Loading animation
```

#### `frontend/index.html`

**Purpose:** HTML template file  
**Contains:**

- Meta tags (charset, viewport, description)
- Title tag
- Root div untuk React mounting
- Script tag untuk main.jsx (Vite)

#### `frontend/vite.config.js`

**Purpose:** Vite bundler configuration  
**Features:**

- React plugin
- Dev server port (3000)
- Proxy untuk API requests ke backend (5000)

#### `frontend/tailwind.config.js`

**Purpose:** Tailwind CSS configuration  
**Custom Colors:**

```javascript
'dark-bg': '#0d0d0d'      // Background
'dark-card': '#1a1a1a'    // Cards
'dark-border': '#2d2d2d'  // Borders
'accent': '#10a37f'       // Primary color
```

#### `frontend/postcss.config.js`

**Purpose:** PostCSS configuration untuk Tailwind  
**Features:**

- Autoprefixer untuk browser compatibility
- Tailwind CSS processing

#### `frontend/package.json`

**Purpose:** Frontend project configuration  
**Scripts:**

- `npm run dev` - Start development server
- `npm run build` - Build untuk production
- `npm run preview` - Preview production build

**Dependencies:**

- react, react-dom
- axios (HTTP client)

**DevDependencies:**

- vite, @vitejs/plugin-react
- tailwindcss, postcss, autoprefixer

---

### Documentation Files

#### `README.md`

**Purpose:** Main project documentation  
**Sections:**

- Features overview
- Project structure
- Quick start guide
- API endpoints reference
- How to use guide
- Integration guidelines
- Customization options
- Tech stack
- Deployment instructions
- Troubleshooting

#### `SETUP_GUIDE.md`

**Purpose:** Detailed setup dan installation instructions  
**Sections:**

- Prerequisites
- Backend setup step-by-step
- Frontend setup step-by-step
- Environment variables
- Features explanation
- File structure
- Customization guide
- Integration dengan real AI APIs
- Deployment guide
- Troubleshooting

#### `DEVELOPMENT_GUIDE.md`

**Purpose:** Guide untuk developers yang ingin modify code  
**Sections:**

- Development environment setup
- Development workflow
- Component architecture
- API integration pattern
- Testing guide
- Debugging tips
- Code examples
- Styling guidelines
- Security considerations
- Contributing guidelines

#### `AI_INTEGRATION_EXAMPLES.js`

**Purpose:** Code examples untuk integrate real AI APIs  
**Contains Examples:**

- OpenAI (GPT-4, GPT-3.5) integration
- Anthropic Claude integration
- Google Gemini integration
- Unified response generation function
- Streaming responses
- Conversation history handling

---

## 🔄 Data Flow

### Chat Flow

```
User Input
    ↓
ChatInput.jsx (onSend)
    ↓
ChatWindow.jsx (handleSendMessage)
    ↓
api.js (chatAPI.sendMessage)
    ↓
Backend POST /api/chat
    ↓
generateAIResponse()
    ↓
Response back to frontend
    ↓
setMessages() update
    ↓
ChatMessage.jsx displays new messages
```

### Model Selection Flow

```
ModelSwitcher.jsx (onModelChange)
    ↓
ChatWindow.jsx (setSelectedModel)
    ↓
State updated
    ↓
Messages dikirim dengan model baru
```

### Initial Load Flow

```
App.jsx loads
    ↓
ChatWindow.jsx mounts
    ↓
useEffect loadModels()
    ↓
api.js getModels()
    ↓
Backend GET /api/models
    ↓
setModels() dengan response
    ↓
ModelSwitcher renders models
```

---

## 💾 Storage

### Backend In-Memory Storage

```javascript
chatHistory = {
  'session_123456': [
    { id: 1, role: 'user', content: '...', timestamp: '...', model: '...' },
    { id: 2, role: 'assistant', content: '...', timestamp: '...', model: '...' },
    // ... more messages
  ],
  'session_789012': [ ... ]
}
```

**Note:** Data hilang setelah server restart. Untuk persistent storage, gunakan database (MongoDB, PostgreSQL, etc).

### Frontend State

```javascript
messages: [array of message objects]
selectedModel: 'gpt-4'
isLoading: false
sessionId: 'session_123456'
```

---

## 🔗 Environment Variables

Buat file `.env` di folder backend:

```env
# Server Configuration
PORT=5000
NODE_ENV=development

# API Keys (Opsional - hanya jika menggunakan real APIs)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIzaSy...

# Frontend (di .env frontend jika perlu)
VITE_API_URL=http://localhost:5000
```

---

## 📦 Package Dependencies

### Backend

- `express` - Web framework
- `cors` - Cross-origin middleware
- `dotenv` - Environment variables
- `axios` - HTTP client
- `nodemon` - Auto-reload (dev)

### Frontend

- `react` - UI library
- `react-dom` - React rendering
- `axios` - HTTP client
- `vite` - Bundler
- `tailwindcss` - CSS framework

### Optional (untuk real AI APIs)

- `openai` - OpenAI API
- `@anthropic-ai/sdk` - Claude API
- `@google/generative-ai` - Gemini API

---

## ✅ Next Steps

1. **Setup** - Follow SETUP_GUIDE.md
2. **Develop** - Use DEVELOPMENT_GUIDE.md
3. **Integrate AI** - Check AI_INTEGRATION_EXAMPLES.js
4. **Deploy** - Follow deployment section di README

---

Happy coding! 🚀
