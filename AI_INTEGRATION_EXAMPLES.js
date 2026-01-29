// Example: Real AI API Integration untuk backend/server.js
// File ini menunjukkan cara mengintegrasikan real AI APIs

// ===========================
// 1. OPENAI INTEGRATION (GPT Models)
// ===========================

/*
// Install terlebih dahulu:
// npm install openai

const { Configuration, OpenAIApi } = require("openai");

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

async function generateOpenAIResponse(message, model) {
  try {
    const completion = await openai.createChatCompletion({
      model: model, // "gpt-4" atau "gpt-3.5-turbo"
      messages: [
        {
          role: "user",
          content: message
        }
      ],
      temperature: 0.7,
      max_tokens: 2000,
    });

    return completion.data.choices[0].message.content;
  } catch (error) {
    console.error("OpenAI Error:", error);
    throw new Error("Failed to get response from OpenAI");
  }
}
*/

// ===========================
// 2. ANTHROPIC CLAUDE INTEGRATION
// ===========================

/*
// Install terlebih dahulu:
// npm install @anthropic-ai/sdk

const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function generateClaudeResponse(message, model) {
  try {
    const response = await client.messages.create({
      model: model, // "claude-3-opus-20240229" atau "claude-3-sonnet-20240229"
      max_tokens: 2000,
      messages: [
        {
          role: "user",
          content: message
        }
      ],
      temperature: 0.7,
    });

    return response.content[0].text;
  } catch (error) {
    console.error("Claude Error:", error);
    throw new Error("Failed to get response from Claude");
  }
}
*/

// ===========================
// 3. GOOGLE GEMINI INTEGRATION
// ===========================

/*
// Install terlebih dahulu:
// npm install @google/generative-ai

const { GoogleGenerativeAI } = require("@google/generative-ai");

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

async function generateGeminiResponse(message, modelName = "gemini-pro") {
  try {
    const model = genAI.getGenerativeModel({ model: modelName });
    
    const result = await model.generateContent({
      contents: [
        {
          parts: [
            {
              text: message
            }
          ],
        }
      ],
    });

    const response = result.response;
    return response.text();
  } catch (error) {
    console.error("Gemini Error:", error);
    throw new Error("Failed to get response from Gemini");
  }
}
*/

// ===========================
// UNIFIED GENERATE RESPONSE FUNCTION
// ===========================

/*
// Ganti fungsi generateAIResponse di server.js dengan ini:

async function generateAIResponse(message, model) {
  if (model.startsWith('gpt')) {
    return await generateOpenAIResponse(message, model);
  } else if (model.startsWith('claude')) {
    return await generateClaudeResponse(message, model);
  } else if (model === 'gemini-pro') {
    return await generateGeminiResponse(message, model);
  } else {
    throw new Error(`Unknown model: ${model}`);
  }
}
*/

// ===========================
// COMPLETE EXAMPLE: Using Multiple APIs
// ===========================

/*
// Tambahkan di backend/server.js after require statements:

const { Configuration, OpenAIApi } = require("openai");
const Anthropic = require("@anthropic-ai/sdk");
const { GoogleGenerativeAI } = require("@google/generative-ai");

// Initialize APIs
const openai = new OpenAIApi(
  new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  })
);

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

// Update generateAIResponse function
async function generateAIResponse(message, model) {
  try {
    let response;

    if (model === 'gpt-4' || model === 'gpt-3.5-turbo') {
      const completion = await openai.createChatCompletion({
        model: model,
        messages: [{ role: "user", content: message }],
        temperature: 0.7,
        max_tokens: 2000,
      });
      response = completion.data.choices[0].message.content;
    } 
    else if (model.startsWith('claude')) {
      const message_response = await anthropic.messages.create({
        model: model,
        max_tokens: 2000,
        messages: [{ role: "user", content: message }],
        temperature: 0.7,
      });
      response = message_response.content[0].text;
    } 
    else if (model === 'gemini-pro') {
      const gemini_model = genAI.getGenerativeModel({ model: "gemini-pro" });
      const result = await gemini_model.generateContent(message);
      response = result.response.text();
    } 
    else {
      throw new Error(`Unknown model: ${model}`);
    }

    return response;
  } catch (error) {
    console.error(`Error with ${model}:`, error);
    throw new Error(`Failed to get response from ${model}`);
  }
}

// Update AVAILABLE_MODELS dengan model yang valid
const AVAILABLE_MODELS = [
  {
    id: 'gpt-4',
    name: 'GPT-4',
    provider: 'openai',
    description: 'Most capable model',
    icon: '🤖'
  },
  {
    id: 'gpt-3.5-turbo',
    name: 'GPT-3.5 Turbo',
    provider: 'openai',
    description: 'Fast and efficient',
    icon: '⚡'
  },
  {
    id: 'claude-3-opus-20240229',
    name: 'Claude 3 Opus',
    provider: 'anthropic',
    description: 'Powerful reasoning',
    icon: '🧠'
  },
  {
    id: 'claude-3-sonnet-20240229',
    name: 'Claude 3 Sonnet',
    provider: 'anthropic',
    description: 'Balanced performance',
    icon: '⚖️'
  },
  {
    id: 'gemini-pro',
    name: 'Gemini Pro',
    provider: 'google',
    description: 'Advanced understanding',
    icon: '✨'
  }
];
*/

// ===========================
// STREAMING RESPONSES (Advanced)
// ===========================

/*
// Untuk streaming responses, update POST /api/chat endpoint:

app.post('/api/chat', async (req, res) => {
  try {
    const { message, model, sessionId } = req.body;

    if (!message || !model) {
      return res.status(400).json({
        success: false,
        error: 'Message and model are required'
      });
    }

    // Validate model
    const modelExists = AVAILABLE_MODELS.find(m => m.id === model);
    if (!modelExists) {
      return res.status(400).json({
        success: false,
        error: 'Invalid model selected'
      });
    }

    // Setup streaming response
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    const session = sessionId || `session_${Date.now()}`;
    if (!chatHistory[session]) {
      chatHistory[session] = [];
    }

    // Add user message
    messageId++;
    const userMessage = {
      id: messageId,
      role: 'user',
      content: message,
      timestamp: new Date(),
      model
    };
    chatHistory[session].push(userMessage);
    res.write(`data: ${JSON.stringify({ type: 'user', message: userMessage })}\n\n`);

    // Generate streaming response
    let fullResponse = '';
    
    // Assuming streaming API call returns chunks
    const stream = await generateStreamingResponse(message, model);
    
    stream.on('data', (chunk) => {
      fullResponse += chunk;
      res.write(`data: ${JSON.stringify({ type: 'chunk', content: chunk })}\n\n`);
    });

    stream.on('end', () => {
      messageId++;
      const assistantMessage = {
        id: messageId,
        role: 'assistant',
        content: fullResponse,
        timestamp: new Date(),
        model
      };
      chatHistory[session].push(assistantMessage);
      
      res.write(`data: ${JSON.stringify({ 
        type: 'complete', 
        message: assistantMessage,
        session 
      })}\n\n`);
      res.end();
    });

    stream.on('error', (error) => {
      res.write(`data: ${JSON.stringify({ type: 'error', error: error.message })}\n\n`);
      res.end();
    });

  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to process chat message'
    });
  }
});
*/

// ===========================
// DENGAN CONTEXT/CONVERSATION HISTORY
// ===========================

/*
async function generateAIResponseWithContext(messages, model) {
  try {
    // messages adalah array dari semua conversation history
    // Format: [{ role: 'user' | 'assistant', content: '...' }, ...]
    
    if (model === 'gpt-4' || model === 'gpt-3.5-turbo') {
      const completion = await openai.createChatCompletion({
        model: model,
        messages: messages, // Pass full conversation history
        temperature: 0.7,
        max_tokens: 2000,
      });
      return completion.data.choices[0].message.content;
    }
    // ... similar untuk claude dan gemini
  } catch (error) {
    throw error;
  }
}

// Update di /api/chat endpoint untuk pass history:
const conversationHistory = chatHistory[session].map(msg => ({
  role: msg.role,
  content: msg.content
}));

const aiResponse = await generateAIResponseWithContext(
  conversationHistory,
  model
);
*/

console.log("This file contains examples of AI API integrations.");
console.log("Copy dan uncomment code sesuai kebutuhan Anda.");
console.log("Jangan lupa setup .env file dengan API keys!");
