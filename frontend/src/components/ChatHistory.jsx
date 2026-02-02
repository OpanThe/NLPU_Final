import React, { useState, useEffect } from 'react';
import { chatAPI } from '../utils/api';

export const ChatHistory = ({ onSelectSession, currentSessionId, onNewChat }) => {
  const [sessions, setSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  useEffect(() => {
    loadSessions();
    const interval = setInterval(loadSessions, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadSessions = async () => {
    try {
      setIsLoading(true);
      const response = await chatAPI.getSessions();
      if (response.data.success) {
        // Filter out sessions with no user messages
        const validSessions = response.data.sessions.filter(session => 
          session.first_message && 
          session.first_message.trim() !== '' &&
          session.message_count >= 2 // At least 1 user message + 1 assistant response
        );
        
        // Map fields for frontend (snake_case to camelCase)
        const mappedSessions = validSessions.map(session => ({
          ...session,
          sessionId: session.session_id,
          lastMessage: session.first_message || session.title || 'Empty conversation'
        }));
        
        setSessions(mappedSessions);
      }
    } catch (error) {
      console.error('Failed to load sessions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    const newSessionId = `session_${Date.now()}`;
    onNewChat(newSessionId);
  };

  const handleDeleteSession = async (sessionId, event) => {
    event.stopPropagation(); // Prevent selecting the session
    setDeleteConfirm(sessionId);
  };

  const confirmDelete = async (sessionId, event) => {
    event.stopPropagation();
    try {
      await chatAPI.clearHistory(sessionId);
      setSessions(sessions.filter(s => (s.sessionId || s.session_id) !== sessionId));
      if (currentSessionId === sessionId) {
        handleNewChat();
      }
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Failed to delete session:', error);
      alert('Failed to delete conversation');
    }
  };

  const cancelDelete = (event) => {
    event.stopPropagation();
    setDeleteConfirm(null);
  };

  return (
    <div style={{
      width: '260px',
      background: 'rgba(15, 12, 41, 0.6)',
      backdropFilter: 'blur(20px)',
      borderRight: '1.5px solid rgba(255, 255, 255, 0.1)',
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      overflowY: 'auto',
      boxShadow: '4px 0 20px rgba(0, 0, 0, 0.4)'
    }}>
      {/* New Chat Button */}
      <button
        onClick={handleNewChat}
        style={{
          margin: '16px 12px',
          padding: '12px 16px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          border: '1.5px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '12px',
          fontWeight: '600',
          fontSize: '14px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '8px',
          boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
        }}
        onMouseEnter={(e) => {
          e.target.style.transform = 'translateY(-2px)';
          e.target.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
          e.target.style.background = 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)';
        }}
        onMouseLeave={(e) => {
          e.target.style.transform = 'translateY(0)';
          e.target.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
          e.target.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }}
      >
        <span style={{
          fontSize: '18px',
          fontWeight: '700',
          color: '#e0e7ff'
        }}>+</span>
        <span>New Chat</span>
      </button>

      {/* Chat History */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '8px' }}>
        <div style={{ 
          fontSize: '11px', 
          color: '#a5b4fc', 
          padding: '12px 8px', 
          fontWeight: '700', 
          letterSpacing: '1.2px',
          textTransform: 'uppercase'
        }}>
          💬 Conversations
        </div>
        
        {sessions.length === 0 ? (
          <div style={{ padding: '20px 12px', fontSize: '13px', color: '#94a3b8', textAlign: 'center' }}>
            No history yet
          </div>
        ) : (
          sessions.map((session) => {
            const isSelected = currentSessionId === session.sessionId;
            const showDeleteConfirm = deleteConfirm === session.sessionId;
            
            return (
              <div key={session.sessionId} style={{ marginBottom: '6px' }}>
                {showDeleteConfirm ? (
                  // Delete Confirmation
                  <div style={{
                    padding: '12px',
                    background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%)',
                    backdropFilter: 'blur(10px)',
                    border: '1.5px solid rgba(239, 68, 68, 0.4)',
                    borderRadius: '10px',
                    color: '#fca5a5',
                    boxShadow: '0 4px 12px rgba(239, 68, 68, 0.3)'
                  }}>
                    <div style={{ fontSize: '12px', marginBottom: '8px', fontWeight: '600' }}>
                      Delete this conversation?
                    </div>
                    <div style={{ display: 'flex', gap: '6px' }}>
                      <button
                        onClick={(e) => confirmDelete(session.sessionId, e)}
                        style={{
                          flex: 1,
                          padding: '8px',
                          background: 'linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)',
                          color: 'white',
                          border: 'none',
                          borderRadius: '6px',
                          fontSize: '11px',
                          fontWeight: '600',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                          boxShadow: '0 2px 8px rgba(220, 38, 38, 0.4)'
                        }}
                        onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'}
                        onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
                      >
                        Delete
                      </button>
                      <button
                        onClick={cancelDelete}
                        style={{
                          flex: 1,
                          padding: '8px',
                          background: 'rgba(255, 255, 255, 0.1)',
                          backdropFilter: 'blur(10px)',
                          color: 'white',
                          border: '1px solid rgba(255, 255, 255, 0.2)',
                          borderRadius: '6px',
                          fontSize: '11px',
                          fontWeight: '600',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease'
                        }}
                        onMouseEnter={(e) => e.target.style.background = 'rgba(255, 255, 255, 0.15)'}
                        onMouseLeave={(e) => e.target.style.background = 'rgba(255, 255, 255, 0.1)'}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  // Session Item
                  <div style={{ display: 'flex', gap: '4px', animation: 'fadeIn 0.3s ease-in-out' }}>
                    <button
                      onClick={() => onSelectSession(session.sessionId)}
                      style={{
                        flex: 1,
                        padding: '10px 12px',
                        background: isSelected 
                          ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%)'
                          : 'transparent',
                        backdropFilter: isSelected ? 'blur(10px)' : 'none',
                        borderLeft: isSelected ? '3px solid #667eea' : '3px solid transparent',
                        color: isSelected ? '#a5b4fc' : '#cbd5e1',
                        border: isSelected 
                          ? '1.5px solid rgba(102, 126, 234, 0.4)'
                          : '1.5px solid transparent',
                        borderRadius: '8px',
                        textAlign: 'left',
                        cursor: 'pointer',
                        fontSize: '13px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                        boxShadow: isSelected ? '0 2px 10px rgba(102, 126, 234, 0.3)' : 'none'
                      }}
                      onMouseEnter={(e) => {
                        if (!isSelected) {
                          e.target.style.background = 'rgba(255, 255, 255, 0.08)';
                          e.target.style.backdropFilter = 'blur(10px)';
                          e.target.style.transform = 'translateX(4px)';
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (!isSelected) {
                          e.target.style.background = 'transparent';
                          e.target.style.backdropFilter = 'none';
                          e.target.style.transform = 'translateX(0)';
                        }
                      }}
                      title={session.lastMessage || 'Empty conversation'}
                    >
                      {(session.lastMessage || 'Empty conversation').substring(0, 28)}...
                    </button>
                    
                    <button
                      onClick={(e) => handleDeleteSession(session.sessionId, e)}
                      style={{
                        padding: '8px',
                        background: 'transparent',
                        color: '#94a3b8',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}
                      onMouseEnter={(e) => {
                        e.target.style.background = 'linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(220, 38, 38, 0.3) 100%)';
                        e.target.style.color = '#f87171';
                        e.target.style.transform = 'scale(1.1) rotate(10deg)';
                      }}
                      onMouseLeave={(e) => {
                        e.target.style.background = 'transparent';
                        e.target.style.color = '#94a3b8';
                        e.target.style.transform = 'scale(1) rotate(0deg)';
                      }}
                      title="Delete conversation"
                    >
                      🗑️
                    </button>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Footer */}
      <div style={{
        padding: '16px 12px',
        borderTop: '1.5px solid rgba(255, 255, 255, 0.1)',
        fontSize: '12px',
        color: '#a5b4fc',
        textAlign: 'center',
        fontWeight: '600',
        background: 'rgba(102, 126, 234, 0.1)',
        backdropFilter: 'blur(10px)',
        letterSpacing: '0.5px'
      }}>
        ✨ Jarvis AI
      </div>
    </div>
  );
};

export default ChatHistory;
