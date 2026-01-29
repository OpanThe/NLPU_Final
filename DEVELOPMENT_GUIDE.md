# Development Guide - ChatBot Application

## 🛠️ Development Environment Setup

### Persyaratan

- Node.js 16.x atau lebih baru
- npm 7.x atau lebih baru (atau yarn)
- Git (untuk version control)
- Code editor (VS Code recommended)

### Step-by-Step Development Setup

#### 1. Clone/Open Project

```bash
cd d:\nlp-final\chatbot-app
```

#### 2. Backend Development

```bash
cd backend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env dan masukkan API keys:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...

# Start development server dengan auto-reload
npm run dev
# atau langsung start
npm start
```

Backend API akan tersedia di: `http://localhost:5000`

#### 3. Frontend Development

Buka terminal baru:

```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

Frontend akan tersedia di: `http://localhost:3000`

## 📝 Development Workflow

### Working on Backend Features

1. **Add new API endpoint** di `backend/server.js`

   ```javascript
   app.post("/api/new-endpoint", (req, res) => {
     // Your code here
     res.json({ success: true, data: {} });
   });
   ```

2. **Update API service** di `frontend/src/utils/api.js`

   ```javascript
   newEndpoint: (params) => api.post('/api/new-endpoint', params),
   ```

3. **Create component** untuk menggunakan endpoint
   ```javascript
   import { chatAPI } from "../utils/api";
   ```

### Working on Frontend Components

1. **Create new component** di `frontend/src/components/`
2. **Import di parent component**
3. **Style dengan Tailwind classes**
4. **Add to App.jsx** jika top-level component

### File Organization

```
frontend/src/
├── components/          # React components
│   └── *.jsx           # Each component in separate file
├── utils/              # Utility functions
│   ├── api.js          # API calls
│   └── helpers.js      # Helper functions (optional)
├── App.jsx             # Main app component
├── main.jsx            # React entry
└── index.css           # Global styles
```

## 🎯 Key Components

### ChatWindow.jsx (Main Container)

- Manage chat state (messages, loading, etc)
- Handle API calls
- Manage model selection
- Render sub-components

```javascript
const [messages, setMessages] = useState([]);
const [selectedModel, setSelectedModel] = useState("gpt-4");
const [isLoading, setIsLoading] = useState(false);
```

### ChatMessage.jsx (Message Display)

- Props: `message`, `isUser`
- Display message content
- Show timestamp dan model
- Different styling untuk user vs assistant

### ChatInput.jsx (Input Form)

- Props: `value`, `onChange`, `onSend`, `isLoading`
- Handle keyboard input (Enter to send)
- Submit button dengan loading state
- Textarea untuk multi-line messages

### ModelSwitcher.jsx (Model Selection)

- Props: `models`, `selectedModel`, `onModelChange`, `isLoading`
- Display available models
- Handle model change
- Disabled state saat loading

## 🔗 API Integration Pattern

```javascript
// 1. Define API call di utils/api.js
export const chatAPI = {
  sendMessage: (message, model, sessionId) =>
    api.post("/api/chat", { message, model, sessionId }),
};

// 2. Use dalam component
import { chatAPI } from "../utils/api";

const handleSend = async () => {
  try {
    const response = await chatAPI.sendMessage(message, model, sessionId);
    // Handle response
  } catch (error) {
    // Handle error
  }
};
```

## 🧪 Testing Locally

### Test Backend API with cURL

```bash
# Test health check
curl http://localhost:5000/api/health

# Get available models
curl http://localhost:5000/api/models

# Send message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "model": "gpt-4",
    "sessionId": "test-session"
  }'
```

### Test Frontend Features

- Open http://localhost:3000 di browser
- Test model switcher
- Send test messages
- Clear chat history
- Check console untuk errors (F12)

## 📦 Adding Dependencies

### Backend

```bash
cd backend
npm install package-name
# Restart server
```

### Frontend

```bash
cd frontend
npm install package-name
# Dev server auto-reloads
```

## 🎨 Styling Guide

### Using Tailwind CSS

```javascript
// Instead of CSS
<div className="flex items-center justify-between p-6 border-b border-gray-200">
  <h1 className="text-2xl font-bold">Title</h1>
  <button className="px-4 py-2 bg-blue-500 text-white rounded">Click me</button>
</div>
```

### Custom Colors (dari config)

```javascript
// dark-bg, dark-card, dark-border, accent sudah tersedia
<div className="bg-dark-bg text-white border border-dark-border">
  Content
</div>

<button className="bg-accent hover:bg-accent/80">
  Action
</button>
```

### Responsive Design

```javascript
<div className="w-full md:w-1/2 lg:w-1/3">
  // w-full di mobile, w-1/2 di tablet, w-1/3 di desktop
</div>
```

## 🐛 Debugging

### Browser DevTools (F12)

- **Console** - Check untuk errors
- **Network** - Monitor API calls
- **Application** - Check local storage
- **Elements** - Inspect HTML structure

### Backend Debugging

```javascript
// Add console logs
console.log("Message:", message);
console.log("Model:", model);

// Use try-catch untuk handle errors
try {
  // Code
} catch (error) {
  console.error("Error details:", error);
}
```

### React DevTools

- Install extension di browser
- Inspect component props dan state
- Check component tree

## 📚 Code Examples

### Creating New API Endpoint

**backend/server.js:**

```javascript
app.post("/api/new-feature", async (req, res) => {
  try {
    const { data } = req.body;

    // Process data
    const result = await processData(data);

    res.json({
      success: true,
      result,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});
```

**frontend/src/utils/api.js:**

```javascript
newFeature: (data) => api.post('/api/new-feature', { data }),
```

**frontend/src/components/MyComponent.jsx:**

```javascript
import { chatAPI } from "../utils/api";

const MyComponent = () => {
  const handleClick = async () => {
    try {
      const response = await chatAPI.newFeature(myData);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return <button onClick={handleClick}>Click</button>;
};
```

### Adding New Component

**frontend/src/components/MyFeature.jsx:**

```javascript
import React, { useState } from "react";

export const MyFeature = ({ prop1, prop2 }) => {
  const [state, setState] = useState(null);

  const handleAction = () => {
    // Do something
  };

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-lg font-bold">My Feature</h2>
      <button
        onClick={handleAction}
        className="px-4 py-2 bg-accent text-white rounded"
      >
        Action Button
      </button>
    </div>
  );
};

export default MyFeature;
```

## 🚀 Performance Tips

1. **Lazy Loading** - Load components only when needed
2. **Memoization** - Use React.memo untuk prevent re-renders
3. **Code Splitting** - Separate large bundles
4. **Image Optimization** - Compress images sebelum upload
5. **API Caching** - Cache frequently used data

## 🔐 Security Considerations

1. **Never commit .env files** - Sensitif data seperti API keys
2. **Validate input** - Backend validation untuk all inputs
3. **CORS** - Configure hanya allowed origins
4. **Rate limiting** - Prevent abuse dengan rate limiting
5. **Authentication** - Add user auth untuk production

## 📖 Additional Resources

- [React 18 Docs](https://react.dev)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Axios Documentation](https://axios-http.com/docs/intro)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes
3. Commit: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Create Pull Request

## ✅ Checklist Sebelum Deploy

- [ ] Test all features locally
- [ ] No console errors
- [ ] Responsive design tested
- [ ] API endpoints tested
- [ ] Environment variables configured
- [ ] Build project: `npm run build`
- [ ] No sensitive data di code
- [ ] Documentation updated

---

Happy coding! 🎉
