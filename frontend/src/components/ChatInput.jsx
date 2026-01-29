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
    <div style={{ padding: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', backgroundColor: '#1a1f3a', background: 'linear-gradient(180deg, #1a1f3a 0%, #0d0d0d 100%)' }}>
      <div style={{ display: 'flex', gap: '12px', maxWidth: '900px', margin: '0 auto' }}>
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message... (Shift+Enter for new line)"
          disabled={isLoading}
          style={{
            flex: 1,
            padding: '12px 16px',
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            borderRadius: '12px',
            color: 'white',
            fontSize: '14px',
            fontFamily: 'inherit',
            resize: 'none',
            opacity: isLoading ? 0.5 : 1,
            outline: 'none',
            transition: 'all 0.3s ease'
          }}
          onFocus={(e) => !isLoading && (e.target.style.borderColor = 'rgba(255, 255, 255, 0.3)', e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.08)', e.target.style.boxShadow = '0 0 0 3px rgba(255, 255, 255, 0.1)')}
          onBlur={(e) => (e.target.style.borderColor = 'rgba(255, 255, 255, 0.15)', e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.05)', e.target.style.boxShadow = 'none')}
          rows="3"
        />
        <button
          type="button"
          onClick={handleButtonClick}
          disabled={isLoading || !value.trim()}
          style={{
            padding: '12px 20px',
            backgroundColor: isLoading || !value.trim() ? 'rgba(100, 100, 100, 0.4)' : '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '12px',
            fontWeight: '600',
            cursor: isLoading || !value.trim() ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            opacity: isLoading || !value.trim() ? 0.6 : 1,
            transition: 'all 0.2s ease',
            outline: 'none'
          }}
          onMouseEnter={(e) => {
            if (!isLoading && value.trim()) {
              e.currentTarget.style.backgroundColor = '#2563eb';
            }
          }}
          onMouseLeave={(e) => {
            if (!isLoading && value.trim()) {
              e.currentTarget.style.backgroundColor = '#3b82f6';
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
