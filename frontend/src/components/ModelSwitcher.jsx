import React from 'react';

export const ModelSwitcher = ({ models, selectedModel, onModelChange, isLoading }) => {
  return (
    <div style={{ padding: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)', backgroundColor: '#1a1f3a' }}>
      <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: '#64748b', marginBottom: '10px', letterSpacing: '0.5px' }}>
        AI MODEL
      </label>
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        {models.map((model) => (
          <button
            key={model.id}
            onClick={() => onModelChange(model.id)}
            disabled={isLoading}
            style={{
              padding: '8px 12px',
              backgroundColor: selectedModel === model.id 
                ? '#333333'
                : 'rgba(255, 255, 255, 0.08)',
              color: selectedModel === model.id ? 'white' : '#cbd5e1',
              border: selectedModel === model.id ? '1px solid #555555' : '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: '500',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1,
              transition: 'all 0.3s ease',
              boxShadow: selectedModel === model.id ? '0 4px 12px rgba(0, 0, 0, 0.4)' : 'none',
              whiteSpace: 'nowrap'
            }}
            onMouseEnter={(e) => {
              if (selectedModel !== model.id && !isLoading) {
                e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.12)';
                e.target.style.transform = 'translateY(-2px)';
              }
            }}
            onMouseLeave={(e) => {
              if (selectedModel !== model.id && !isLoading) {
                e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.08)';
                e.target.style.transform = 'translateY(0)';
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
