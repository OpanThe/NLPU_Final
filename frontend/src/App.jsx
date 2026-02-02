import React from 'react';
import ChatWindow from './components/ChatWindow';
import './index.css';

function App() {
  console.log('App rendering with ChatWindow...');
  
  try {
    return (
      <div style={{ 
        height: '100vh', 
        width: '100vw', 
        background: 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
        backgroundAttachment: 'fixed'
      }}>
        <ChatWindow />
      </div>
    );
  } catch (error) {
    console.error('App Error:', error);
    return (
      <div style={{ color: 'white', padding: '20px' }}>
        Error: {error.message}
      </div>
    );
  }
}

export default App;
