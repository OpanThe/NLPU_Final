import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  getModels: () => api.get('/api/models'),
  
  getGreeting: (model) => api.get('/api/greeting', { params: { model } }),
  
  sendMessage: (message, model, sessionId) =>
    api.post('/api/chat', { message, model, sessionId }),
  
  getChatHistory: (sessionId) =>
    api.get(`/api/chat-history/${sessionId}`),
  
  clearHistory: (sessionId) =>
    api.delete(`/api/chat-history/${sessionId}`),
  
  getSessions: () =>
    api.get('/api/sessions'),
  
  healthCheck: () =>
    api.get('/api/health'),
};

export default api;
