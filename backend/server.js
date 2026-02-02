const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');
const axios = require('axios');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage untuk chat history
const chatHistory = {};
let messageId = 0;

// Available AI Models - Gemini, Llama 3.2, and Qwen 2.5
const AVAILABLE_MODELS = [
  {
    id: 'llama',
    name: 'Llama 3.2 3B',
    provider: 'local',
    description: 'Fine-tuned - Fast & Private',
    icon: '🦙'
  },
  {
    id: 'qwen',
    name: 'Qwen 2.5 3B',
    provider: 'local',
    description: 'Fine-tuned - Best Performance',
    icon: '💉'
  },
  {
    id: 'gemini',
    name: 'Gemini 2.5 Flash',
    provider: 'google',
    description: 'Cloud-based Google AI',
    icon: '✨'
  }
];

// Python Backend Integration
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

// AI Response Generator - Calls Python FastAPI backend
async function generateAIResponse(message, model) {
  try {
    // Call Python FastAPI backend
    const response = await axios.post(`${PYTHON_BACKEND_URL}/chat`, {
      question: message,
      model_type: model  // 'llama' or 'gemini'
    });

    return response.data.answer;
  } catch (error) {
    console.error('Error calling Python backend:', error.message);
    
    // Fallback error message
    if (error.response) {
      throw new Error(`AI Error: ${error.response.data.detail || 'Failed to get response'}`);
    } else if (error.request) {
      throw new Error('Cannot connect to AI backend. Please ensure Python backend is running on port 8000.');
    } else {
      throw new Error(`Error: ${error.message}`);
    }
  }
}

// Routes

// Get available models
app.get('/api/models', (req, res) => {
  res.json({
    success: true,
    models: AVAILABLE_MODELS
  });
});

// Get greeting with suggested questions
app.get('/api/greeting', async (req, res) => {
  try {
    const { model } = req.query;
    const modelType = model || 'llama';

    // Call Python backend for greeting
    const response = await axios.get(`${PYTHON_BACKEND_URL}/greeting`, {
      params: { model_type: modelType }
    });

    res.json({
      success: true,
      ...response.data
    });
  } catch (error) {
    console.error('Greeting error:', error.message);
    // Fallback greeting with sample questions if backend fails
    const fallbackQuestions = [
      "Can I meet representative from Academic Bureau to consult matters regarding my studies?",
      "What if I missed the deadline for enrollment?",
      "Can I drop the subjects or classes that I have been enrolled in?",
      "Why can't I access my GPA?",
      "Can I change my major?",
      "What if I want to transfer to President University?"
    ];
    
    // Randomly select 4 questions
    const shuffled = fallbackQuestions.sort(() => 0.5 - Math.random());
    const selected = shuffled.slice(0, 4);
    
    res.json({
      success: true,
      greeting: "Hello! I'm Jarvis AI, your friendly assistant for President University! 😊\n\nI can help you with information about the university. Here are some questions you might want to ask:",
      suggested_questions: selected,
      source: modelType === 'gemini' ? 'Gemini 2.5 Flash' : 
              modelType === 'qwen' ? 'Qwen 2.5 3B (Fine-tuned)' : 
              'Llama 3.2 3B (Fine-tuned)'
    });
  }
});

// Chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { message, model, sessionId } = req.body;

    if (!message || !model) {
      return res.status(400).json({
        success: false,
        error: 'Message and model are required'
      });
    }

    // Validate model exists
    const modelExists = AVAILABLE_MODELS.find(m => m.id === model);
    if (!modelExists) {
      return res.status(400).json({
        success: false,
        error: 'Invalid model selected'
      });
    }

    // Initialize session if not exists
    const session = sessionId || `session_${Date.now()}`;
    if (!chatHistory[session]) {
      chatHistory[session] = [];
    }

    // Add user message to history
    messageId++;
    const userMessage = {
      id: messageId,
      role: 'user',
      content: message,
      timestamp: new Date(),
      model
    };
    chatHistory[session].push(userMessage);

    // Generate AI response with session_id
    const response = await axios.post(`${PYTHON_BACKEND_URL}/chat`, {
      question: message,
      model_type: model,
      session_id: session  // Pass session_id to backend
    });
    
    const aiResponse = response.data.answer;

    messageId++;
    const assistantMessage = {
      id: messageId,
      role: 'assistant',
      content: aiResponse,
      timestamp: new Date(),
      model
    };
    chatHistory[session].push(assistantMessage);

    res.json({
      success: true,
      session,
      messages: [userMessage, assistantMessage],
      history: chatHistory[session]
    });

  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to process chat message',
      details: error.message
    });
  }
});

// Get chat history
app.get('/api/chat-history/:sessionId', (req, res) => {
  try {
    const { sessionId } = req.params;
    const history = chatHistory[sessionId] || [];

    res.json({
      success: true,
      sessionId,
      history
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch chat history'
    });
  }
});

// Clear chat history
app.delete('/api/chat-history/:sessionId', (req, res) => {
  try {
    const { sessionId } = req.params;
    delete chatHistory[sessionId];

    res.json({
      success: true,
      message: 'Chat history cleared'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to clear chat history'
    });
  }
});

// Get all sessions
app.get('/api/sessions', async (req, res) => {
  try {
    // Proxy to Python backend for database sessions
    const response = await axios.get(`${PYTHON_BACKEND_URL}/sessions`);
    res.json(response.data);
  } catch (error) {
    console.error('Sessions error:', error.message);
    // Fallback to in-memory sessions
    const sessions = Object.keys(chatHistory).map(sessionId => ({
      sessionId,
      messageCount: chatHistory[sessionId].length,
      lastMessage: chatHistory[sessionId][chatHistory[sessionId].length - 1]?.content || '',
      lastTimestamp: chatHistory[sessionId][chatHistory[sessionId].length - 1]?.timestamp || null
    }));

    res.json({
      success: true,
      sessions
    });
  }
});

// Get messages from specific session
app.get('/api/session/:sessionId/messages', async (req, res) => {
  try {
    const { sessionId } = req.params;
    // Proxy to Python backend
    const response = await axios.get(`${PYTHON_BACKEND_URL}/session/${sessionId}/messages`);
    res.json(response.data);
  } catch (error) {
    console.error('Get messages error:', error.message);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch messages'
    });
  }
});

// Delete session
app.delete('/api/session/:sessionId', async (req, res) => {
  try {
    const { sessionId } = req.params;
    // Proxy to Python backend
    const response = await axios.delete(`${PYTHON_BACKEND_URL}/session/${sessionId}`);
    
    // Also clear from in-memory cache
    delete chatHistory[sessionId];
    
    res.json(response.data);
  } catch (error) {
    console.error('Delete session error:', error.message);
    res.status(500).json({
      success: false,
      error: 'Failed to delete session'
    });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    status: 'Server is running',
    timestamp: new Date()
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    error: 'Internal server error'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 ChatBot Backend running on http://localhost:${PORT}`);
  console.log(`📝 API Documentation:`);
  console.log(`   GET  /api/health - Health check`);
  console.log(`   GET  /api/models - Get available models`);
  console.log(`   POST /api/chat - Send chat message`);
  console.log(`   GET  /api/chat-history/:sessionId - Get chat history`);
  console.log(`   DELETE /api/chat-history/:sessionId - Clear chat history`);
  console.log(`   GET  /api/sessions - Get all sessions`);
});

module.exports = app;
