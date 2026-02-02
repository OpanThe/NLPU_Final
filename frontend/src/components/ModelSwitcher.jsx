import React from 'react';

export const ModelSwitcher = ({ models, selectedModel, onModelChange, isLoading }) => {
  return (
    <div style={{ 
      padding: '20px', 
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)', 
      background: 'rgba(15, 12, 41, 0.6)',
      backdropFilter: 'blur(10px)'
    }}>
      <label style={{ 
        display: 'block', 
        fontSize: '11px', 
        fontWeight: '700', 
        color: '#94a3b8', 
        marginBottom: '12px', 
        letterSpacing: '1.2px',
        textTransform: 'uppercase'
      }}>
        🤖 AI Model
      </label>
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        {models.map((model) => (
          <button
            key={model.id}
            onClick={() => onModelChange(model.id)}
            disabled={isLoading}
            style={{
              padding: '10px 16px',
              background: selectedModel === model.id 
                ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                : 'rgba(255, 255, 255, 0.08)',
              color: selectedModel === model.id ? 'white' : '#cbd5e1',
              border: selectedModel === model.id 
                ? '1.5px solid rgba(102, 126, 234, 0.4)' 
                : '1.5px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '12px',
              fontSize: '13px',
              fontWeight: '600',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1,
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              boxShadow: selectedModel === model.id 
                ? '0 4px 15px rgba(102, 126, 234, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1) inset' 
                : '0 2px 8px rgba(0, 0, 0, 0.2)',
              whiteSpace: 'nowrap',
              backdropFilter: 'blur(10px)'
            }}
            onMouseEnter={(e) => {
              if (selectedModel !== model.id && !isLoading) {
                e.target.style.background = 'rgba(255, 255, 255, 0.15)';
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.3)';
                e.target.style.borderColor = 'rgba(255, 255, 255, 0.2)';
              }
            }}
            onMouseLeave={(e) => {
              if (selectedModel !== model.id && !isLoading) {
                e.target.style.background = 'rgba(255, 255, 255, 0.08)';
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.2)';
                e.target.style.borderColor = 'rgba(255, 255, 255, 0.1)';
              }
            }}
            title={model.description}
          >
            {model.icon} {model.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ModelSwitcher;
