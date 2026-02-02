import React from 'react';

// Function to parse and format markdown text
const parseMarkdown = (text) => {
  if (!text) return '';
  
  let formatted = text;
  
  // Convert **bold** to <strong>
  formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  
  // Convert *italic* to <em>
  formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');
  
  // Convert bullet points
  formatted = formatted.replace(/^[\*\-]\s+(.+)$/gm, '<li>$1</li>');
  
  // Wrap consecutive list items in <ul>
  formatted = formatted.replace(/(<li>.*<\/li>\n?)+/g, (match) => `<ul style="margin: 8px 0; padding-left: 20px;">${match}</ul>`);
  
  // Convert ### headers to h3
  formatted = formatted.replace(/^###\s+(.+)$/gm, '<h3 style="font-size: 16px; font-weight: 600; margin: 12px 0 8px 0;">$1</h3>');
  
  // Convert ## headers to h2
  formatted = formatted.replace(/^##\s+(.+)$/gm, '<h2 style="font-size: 18px; font-weight: 600; margin: 14px 0 10px 0;">$1</h2>');
  
  // Convert line breaks to <br>
  formatted = formatted.replace(/\n/g, '<br />');
  
  return formatted;
};

export const ChatMessage = ({ message, isUser, onQuestionClick }) => {
  const timeStr = new Date(message.timestamp).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  });

  // Check if this is a loading message
  const isLoadingMessage = message.isLoading || message.content === 'typing';

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: isUser ? 'flex-end' : 'flex-start', 
      marginBottom: '20px', 
      paddingX: '16px',
      animation: isUser ? 'slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1)' : 'slideInLeft 0.4s cubic-bezier(0.4, 0, 0.2, 1)'
    }}>
      <div style={{
        borderRadius: '16px',
        padding: '14px 16px',
        maxWidth: '560px',
        background: isUser 
          ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
          : 'rgba(45, 45, 45, 0.6)',
        backdropFilter: !isUser ? 'blur(20px)' : 'none',
        color: 'white',
        wordWrap: 'break-word',
        boxShadow: isUser 
          ? '0 4px 15px rgba(102, 126, 234, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1) inset'
          : '0 4px 15px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05) inset',
        border: isUser 
          ? '1.5px solid rgba(255, 255, 255, 0.2)'
          : '1.5px solid rgba(255, 255, 255, 0.1)'
      }}>
        {isLoadingMessage ? (
          // Typing indicator animation
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px',
            fontSize: '14px',
            color: '#94a3b8'
          }}>
            <span>🤖 Jarvis AI is thinking</span>
            <div style={{ display: 'flex', gap: '4px' }}>
              <span style={{ 
                animation: 'bounce 1.4s infinite ease-in-out',
                animationDelay: '0s'
              }}>.</span>
              <span style={{ 
                animation: 'bounce 1.4s infinite ease-in-out',
                animationDelay: '0.2s'
              }}>.</span>
              <span style={{ 
                animation: 'bounce 1.4s infinite ease-in-out',
                animationDelay: '0.4s'
              }}>.</span>
            </div>
          </div>
        ) : (
          <>
            <div 
              style={{ 
                fontSize: '14px', 
                lineHeight: '1.5', 
                margin: '0', 
                fontWeight: '400'
              }}
              dangerouslySetInnerHTML={{ __html: parseMarkdown(message.content) }}
            />
            
            {/* Suggested Questions */}
            {message.suggestedQuestions && message.suggestedQuestions.length > 0 && (
              <div style={{ marginTop: '16px' }}>
                {message.suggestedQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => onQuestionClick && onQuestionClick(question)}
                    style={{
                      display: 'block',
                      width: '100%',
                      textAlign: 'left',
                      padding: '12px 16px',
                      marginTop: '8px',
                      background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%)',
                      backdropFilter: 'blur(10px)',
                      border: '1.5px solid rgba(102, 126, 234, 0.3)',
                      borderRadius: '10px',
                      color: '#a5b4fc',
                      fontSize: '13px',
                      cursor: 'pointer',
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                      fontWeight: '500',
                      boxShadow: '0 2px 8px rgba(102, 126, 234, 0.1)'
                    }}
                    onMouseEnter={(e) => {
                      e.target.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%)';
                      e.target.style.borderColor = 'rgba(102, 126, 234, 0.5)';
                      e.target.style.transform = 'translateX(4px)';
                      e.target.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.25)';
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%)';
                      e.target.style.borderColor = 'rgba(102, 126, 234, 0.3)';
                      e.target.style.transform = 'translateX(0)';
                      e.target.style.boxShadow = '0 2px 8px rgba(102, 126, 234, 0.1)';
                    }}
                  >
                    💡 {question}
                  </button>
                ))}
              </div>
            )}
          </>
        )}
        
        {!isLoadingMessage && (
          <div style={{ 
            display: 'flex', 
            justifyContent: 'flex-end', 
            alignItems: 'center', 
            gap: '8px', 
            marginTop: '8px', 
            paddingTop: '8px', 
            borderTop: `1px solid ${isUser ? 'rgba(255,255,255,0.3)' : 'rgba(255,255,255,0.1)'}`, 
            fontSize: '11px', 
            opacity: 0.8 
          }}>
            <span style={{ fontWeight: '500' }}>{timeStr}</span>
            {isUser ? (
              <span style={{ 
                background: 'rgba(255, 255, 255, 0.2)', 
                padding: '3px 10px', 
                borderRadius: '8px',
                fontSize: '10px',
                fontWeight: '600',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                You
              </span>
            ) : message.model && (
              <span style={{ 
                background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%)', 
                padding: '3px 10px', 
                borderRadius: '8px',
                fontSize: '10px',
                fontWeight: '600',
                textTransform: 'uppercase',
                letterSpacing: '0.5px',
                border: '1px solid rgba(102, 126, 234, 0.3)'
              }}>
                {message.model}
              </span>
            )}
          </div>
        )}
      </div>
      
      {/* CSS Animation for typing dots */}
      <style>{`
        @keyframes bounce {
          0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.4;
          }
          30% {
            transform: translateY(-8px);
            opacity: 1;
          }
        }
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default ChatMessage;
