# 🚀 Quick Reference Guide

## Installation & Setup

### Windows

```batch
# Buka PowerShell atau Command Prompt
# Navigate ke project folder
cd d:\nlp-final\chatbot-app

# Double-click start.bat atau run:
start.bat

# Atau manual setup:
cd backend
npm install
copy .env.example .env
npm start

# Terminal baru:
cd frontend
npm install
npm run dev
```

### macOS / Linux

```bash
# Navigate ke project folder
cd d:/nlp-final/chatbot-app

# Run start script
bash start.sh

# Atau manual setup:
cd backend
npm install
cp .env.example .env
npm run dev

# Terminal baru:
cd frontend
npm install
npm run dev
```

## URLs

| Service  | URL                              |
| -------- | -------------------------------- |
| Frontend | http://localhost:3000            |
| Backend  | http://localhost:5000            |
| API Docs | http://localhost:5000/api/health |

## Common Commands

### Backend Commands

```bash
cd backend

# Install dependencies
npm install

# Development mode (auto-reload)
npm run dev

# Production mode
npm start

# Install specific package
npm install package-name

# Uninstall package
npm uninstall package-name
```

### Frontend Commands

```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install specific package
npm install package-name
```

## API Endpoints Reference

### Models

```bash
# Get available models
curl http://localhost:5000/api/models
```

### Chat

```bash
# Send message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "model": "gpt-4",
    "sessionId": "test-session"
  }'
```

### History

```bash
# Get chat history
curl http://localhost:5000/api/chat-history/test-session

# Clear chat history
curl -X DELETE http://localhost:5000/api/chat-history/test-session
```

### Sessions

```bash
# Get all sessions
curl http://localhost:5000/api/sessions
```

### Health

```bash
# Check server health
curl http://localhost:5000/api/health
```

## Environment Variables Setup

### Backend `.env` File

```env
# Required
PORT=5000
NODE_ENV=development

# Optional - Add your API keys for real integrations
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=AIzaSy-your-key-here
```

**How to create:**

1. Go to `backend/` folder
2. Copy `cp .env.example .env` (or copy file manually on Windows)
3. Edit `.env` dan add your API keys
4. Never commit `.env` file to Git!

## Troubleshooting

### Port Already in Use

```bash
# Windows - Find process using port
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux - Find and kill process
lsof -ti:5000 | xargs kill -9
```

### Module Not Found Error

```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CORS Error

- Ensure backend running di http://localhost:5000
- Check `server.js` has `app.use(cors())`
- Check `vite.config.js` proxy is correct

### Frontend Won't Connect to Backend

- Check backend is running (`npm run dev` di backend folder)
- Check both ports (3000 dan 5000) correct
- Check firewall settings
- Open browser console (F12) untuk see error

### Node Modules Too Large

```bash
# Remove node_modules dari Git tracking
git rm -r --cached node_modules
echo "node_modules/" >> .gitignore
git add .gitignore
git commit -m "Remove node_modules from tracking"
```

## Project Structure Quick Reference

```
chatbot-app/
├── backend/              ← Backend server (Express)
│   ├── server.js        ← Main API file
│   └── .env            ← Environment config (CREATE THIS)
│
├── frontend/             ← React frontend
│   ├── src/
│   │   └── components/  ← React components
│   ├── vite.config.js  ← Dev server config
│   └── index.html      ← Entry HTML
│
├── README.md           ← Main documentation
├── SETUP_GUIDE.md      ← Installation guide
├── start.bat          ← Windows quick start
└── start.sh           ← Linux/Mac quick start
```

## File Quick Reference

| File                                        | Purpose              |
| ------------------------------------------- | -------------------- |
| `backend/server.js`                         | Express API server   |
| `backend/.env`                              | API keys & config    |
| `frontend/src/App.jsx`                      | React root component |
| `frontend/src/components/ChatWindow.jsx`    | Main chat UI         |
| `frontend/src/components/ModelSwitcher.jsx` | Model selector       |
| `frontend/src/utils/api.js`                 | API client           |
| `frontend/vite.config.js`                   | Dev server config    |
| `frontend/tailwind.config.js`               | Styling config       |

## Git Workflow

```bash
# Initialize git (jika belum)
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial chatbot project"

# Check status
git status

# View history
git log --oneline
```

## Install AI API SDKs

```bash
cd backend

# OpenAI
npm install openai

# Anthropic Claude
npm install @anthropic-ai/sdk

# Google Gemini
npm install @google/generative-ai
```

Then see `AI_INTEGRATION_EXAMPLES.js` untuk usage examples.

## Performance Tips

1. **Clear browser cache:** Ctrl+Shift+Delete (or Cmd+Shift+Delete macOS)
2. **Hard refresh:** Ctrl+F5 (or Cmd+Shift+R macOS)
3. **Check Network tab:** F12 → Network untuk see API calls
4. **Enable DevTools logging:** F12 → Console

## Extension & Customization

### Add New Model

Edit `backend/server.js`:

```javascript
AVAILABLE_MODELS.push({
  id: "new-model-id",
  name: "New Model",
  provider: "provider",
  description: "Description",
  icon: "🆕",
});
```

### Change Theme Colors

Edit `frontend/tailwind.config.js`:

```javascript
colors: {
  'dark-bg': '#0d0d0d',    // Change background
  'dark-card': '#1a1a1a',  // Change card color
  'accent': '#10a37f'      // Change accent color
}
```

### Add Custom Style

Edit `frontend/src/index.css` dan tambah CSS classes

## Documentation Files

- 📖 **README.md** - Overview & features
- 📖 **SETUP_GUIDE.md** - Installation steps
- 📖 **DEVELOPMENT_GUIDE.md** - For developers
- 📖 **PROJECT_STRUCTURE.md** - File explanations
- 📖 **AI_INTEGRATION_EXAMPLES.js** - API integration examples
- 📖 **QUICK_REFERENCE.md** - This file

## Support

- Check documentation files first
- Search error message di Google
- Check GitHub issues untuk similar problems
- See console errors (F12)

## Useful Links

- [Node.js](https://nodejs.org/)
- [React Docs](https://react.dev)
- [Express Guide](https://expressjs.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Vite Guide](https://vitejs.dev)
- [OpenAI API](https://platform.openai.com/docs)
- [Claude API](https://docs.anthropic.com)
- [Gemini API](https://ai.google.dev)

---

**Ready to start? Run `start.bat` (Windows) or `bash start.sh` (Linux/Mac)!** 🚀
