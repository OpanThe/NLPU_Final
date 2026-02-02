import React from 'react';

export const ChatInput = ({ value, onChange, onSend, isLoading }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  const handleButtonClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isLoading && value.trim()) {
      onSend();
    }
  };

  return (
    <div style={{ 
      padding: '24px', 
      borderTop: '1px solid rgba(255, 255, 255, 0.1)', 
      background: 'rgba(15, 12, 41, 0.8)',
      backdropFilter: 'blur(20px)',
      boxShadow: '0 -4px 20px rgba(0, 0, 0, 0.3)'
    }}>
      <div style={{ display: 'flex', gap: '12px', maxWidth: '900px', margin: '0 auto' }}>
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message... (Shift+Enter for new line)"
          disabled={isLoading}
          style={{
            flex: 1,
            padding: '14px 18px',
            background: 'rgba(255, 255, 255, 0.08)',
            border: '1.5px solid rgba(255, 255, 255, 0.15)',
            borderRadius: '16px',
            color: 'white',
            fontSize: '15px',
            fontFamily: 'inherit',
            resize: 'none',
            opacity: isLoading ? 0.5 : 1,
            outline: 'none',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)'
          }}
          onFocus={(e) => !isLoading && (e.target.style.borderColor = 'rgba(102, 126, 234, 0.6)', e.target.style.background = 'rgba(255, 255, 255, 0.12)', e.target.style.boxShadow = '0 0 0 4px rgba(102, 126, 234, 0.15), 0 8px 20px rgba(0, 0, 0, 0.3)', e.target.style.transform = 'translateY(-1px)')}
          onBlur={(e) => (e.target.style.borderColor = 'rgba(255, 255, 255, 0.15)', e.target.style.background = 'rgba(255, 255, 255, 0.08)', e.target.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)', e.target.style.transform = 'translateY(0)')}
          rows="3"
        />
        <button
          type="button"
          onClick={handleButtonClick}
          disabled={isLoading || !value.trim()}
          style={{
            padding: '12px 24px',
            background: isLoading || !value.trim() 
              ? 'rgba(100, 100, 100, 0.4)' 
              : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            border: 'none',
            borderRadius: '16px',
            fontWeight: '600',
            fontSize: '15px',
            cursor: isLoading || !value.trim() ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            opacity: isLoading || !value.trim() ? 0.6 : 1,
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            outline: 'none',
            boxShadow: isLoading || !value.trim() ? 'none' : '0 4px 15px rgba(102, 126, 234, 0.4)',
            minWidth: '100px'
          }}
          onMouseEnter={(e) => {
            if (!isLoading && value.trim()) {
              e.currentTarget.style.background = 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
            }
          }}
          onMouseLeave={(e) => {
            if (!isLoading && value.trim()) {
              e.currentTarget.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
            }
          }}
        >
          {isLoading ? (
            <>
              <span style={{ display: 'inline-flex', gap: '4px', alignItems: 'center' }}>
                <span style={{ width: '8px', height: '8px', backgroundColor: '#cbd5e1', borderRadius: '50%', animation: 'bounce 1.4s infinite' }}></span>
                <span style={{ width: '8px', height: '8px', backgroundColor: '#cbd5e1', borderRadius: '50%', animation: 'bounce 1.4s infinite 0.2s' }}></span>
                <span style={{ width: '8px', height: '8px', backgroundColor: '#cbd5e1', borderRadius: '50%', animation: 'bounce 1.4s infinite 0.4s' }}></span>
              </span>
            </>
          ) : (
            <>
              <span>Send</span>
              <svg style={{ width: '16px', height: '16px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7m0 0l-7 7m7-7H6" />
              </svg>
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
