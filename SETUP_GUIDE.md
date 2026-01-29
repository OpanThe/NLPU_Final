# Setup Guide - ChatBot Application

## Prerequisites

- Node.js v16+ (Download dari https://nodejs.org/)
- npm atau yarn package manager

## Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Create .env file
# Copy dari .env.example dan isi dengan API keys Anda
cp .env.example .env

# Start server
npm start
```

Backend akan berjalan di `http://localhost:5000`

API Endpoints:

- `GET /api/health` - Health check
- `GET /api/models` - Get available models
- `POST /api/chat` - Send message to AI
- `GET /api/chat-history/:sessionId` - Get chat history
- `DELETE /api/chat-history/:sessionId` - Clear history

### 2. Frontend Setup

Buka terminal baru:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend akan berjalan di `http://localhost:3000`

## Features

### 🤖 AI Model Switcher

Pilih dari berbagai AI model:

- **GPT-4** - Model paling powerful
- **GPT-3.5 Turbo** - Cepat dan efisien
- **Claude 3 Opus** - Reasoning yang powerful
- **Claude 3 Sonnet** - Balanced performance
- **Gemini Pro** - Advanced understanding

### 💬 Chat Interface

- Modern UI mirip ChatGPT
- Real-time message streaming
- Message history per session
- Timestamp untuk setiap pesan
- Model indicator di setiap response

### 🔄 Session Management

- Automatic session tracking
- Save chat history
- Clear chat history
- Multiple session support

### 📱 Responsive Design

- Mobile-friendly interface
- Optimized untuk tablet dan desktop
- Dark mode theme (default)

## Integrating Real AI APIs

### OpenAI Integration

```javascript
// Install package
npm install openai

// Update backend/server.js untuk gunakan real API
const { Configuration, OpenAIApi } = require("openai");

const openai = new OpenAIApi(
  new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  })
);

// Di generateAIResponse function
const response = await openai.createChatCompletion({
  model: model,
  messages: [{ role: "user", content: message }],
});
```

### Anthropic (Claude) Integration

```javascript
// Install package
npm install @anthropic-ai/sdk

// Update backend untuk gunakan Claude API
const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Call API
const response = await client.messages.create({
  model: model,
  max_tokens: 1024,
  messages: [{ role: "user", content: message }],
});
```

### Google Gemini Integration

```javascript
// Install package
npm install @google/generative-ai

// Update backend
const { GoogleGenerativeAI } = require("@google/generative-ai");

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({ model: modelName });

const response = await model.generateContent(message);
```

## File Structure

```
chatbot-app/
├── backend/
│   ├── server.js              # Express server & API endpoints
│   ├── package.json           # Backend dependencies
│   ├── .env.example           # Environment variables template
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx     # Main chat container
│   │   │   ├── ChatMessage.jsx    # Message component
│   │   │   ├── ChatInput.jsx      # Input form
│   │   │   └── ModelSwitcher.jsx  # Model selection dropdown
│   │   ├── utils/
│   │   │   └── api.js             # API service layer
│   │   ├── App.jsx                # Main app component
│   │   ├── main.jsx               # React entry point
│   │   └── index.css              # Global styles & Tailwind
│   ├── index.html             # HTML template
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS config
│   ├── package.json           # Frontend dependencies
│   └── .gitignore
│
└── README.md                  # Project documentation
```

## Customization

### Mengubah Warna Theme

Edit `frontend/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      'dark-bg': '#0d0d0d',      // Background color
      'dark-card': '#1a1a1a',    // Card color
      'dark-border': '#2d2d2d',  // Border color
      'accent': '#10a37f',       // Accent color (tombol)
    }
  },
}
```

### Menambah Model Baru

Edit `backend/server.js`:

```javascript
const AVAILABLE_MODELS = [
  // ... existing models
  {
    id: "your-model-id",
    name: "Your Model Name",
    provider: "provider-name",
    description: "Model description",
    icon: "🆕",
  },
];
```

### Mengubah Styling

Edit `frontend/src/index.css` untuk custom CSS atau Tailwind classes.

## Troubleshooting

### Port sudah digunakan

```bash
# Backend (ganti port di .env)
PORT=5001

# Frontend (di vite.config.js)
server: {
  port: 3001,
}
```

### CORS Error

Pastikan backend CORS middleware sudah aktif:

```javascript
app.use(cors());
```

### Module not found error

```bash
# Bersihkan node_modules dan install ulang
rm -rf node_modules
npm install
```

## Deployment

### Deployment Frontend (Vercel/Netlify)

```bash
npm run build
# Upload dist/ folder ke Vercel/Netlify
```

### Deployment Backend (Heroku/Railway)

```bash
# Push ke git repository
# Connect dengan hosting platform
# Set environment variables
# Deploy!
```

## Support & Resources

- [React Documentation](https://react.dev)
- [Express.js Documentation](https://expressjs.com)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [Vite Documentation](https://vitejs.dev)
- [OpenAI API](https://platform.openai.com/docs)
- [Anthropic Claude API](https://docs.anthropic.com)
- [Google Gemini API](https://ai.google.dev)

## License

MIT License - Feel free to use for personal and commercial projects
