import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import axios from 'axios';

// OpenAI package import (but we'll use it only if needed for frontend)
// import { OpenAI } from 'openai';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [userId] = useState(() => {
    const storedId = localStorage.getItem('userId');
    if (!storedId) {
      const newId = `user_${Date.now()}`;
      localStorage.setItem('userId', newId);
      return newId;
    }
    return storedId;
  });

  const API_BASE_URL = 'http://localhost:8000';
  const messagesEndRef = useRef(null);

  // Initial welcome message
  useEffect(() => {
    setMessages([{
      id: 1,
      text: "🤖 Hello! I'm your AI Todo Assistant powered by Gemini AI. I can help you manage tasks with natural language.",
      sender: 'ai',
      timestamp: new Date()
    }]);
  }, []);

  // Auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Send message to backend
  const sendMessage = async (text) => {
    if (!text.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: text,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      // Call your FastAPI backend (which uses Gemini)
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        message: text,
        user_id: userId,
        conversation_id: 1
      });

      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'ai',
        timestamp: new Date(),
        tool_calls: response.data.tool_calls || [],
        suggested_actions: response.data.suggested_actions || []
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "❌ Error connecting to backend. Make sure server is running: http://localhost:8000",
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  // Handle form submit
  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
    setInput('');
  };

  // Quick action buttons
  const quickActions = [
    { text: "Add task: Buy groceries", emoji: "🛒" },
    { text: "Show pending tasks", emoji: "📋" },
    { text: "List all my tasks", emoji: "📝" },
    { text: "Add: Complete project by Friday", emoji: "🎯" }
  ];

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <h1>🤖 AI Todo Chatbot</h1>
        <div className="subtitle">
          <span className="tag ai-tag">Gemini AI Powered</span>
          <span className="tag user-tag">User: {userId}</span>
        </div>
        <p className="description">
          Natural language task management with Gemini AI
        </p>
      </header>

      {/* Main Content */}
      <div className="main-content">
        {/* Chat Panel */}
        <div className="chat-panel">
          <div className="messages-container">
            {messages.map((msg) => (
              <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
                <div className="message-bubble">
                  <div className="message-header">
                    <span className="sender-icon">
                      {msg.sender === 'user' ? '👤' : '🤖'}
                    </span>
                    <span className="sender-name">
                      {msg.sender === 'user' ? 'You' : 'AI Assistant'}
                    </span>
                    <span className="timestamp">
                      {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <div className="message-text">{msg.text}</div>
                  
                  {/* Tool Calls Display */}
                  {msg.tool_calls && msg.tool_calls.length > 0 && (
                    <div className="tool-calls">
                      <div className="tool-header">
                        <span className="tool-icon">🛠️</span>
                        <span className="tool-title">Actions:</span>
                      </div>
                      {msg.tool_calls.map((tool, idx) => (
                        <div key={idx} className="tool-item">
                          {tool.tool === 'add_task' && `✅ Added: ${tool.title}`}
                          {tool.tool === 'list_tasks' && `📋 Listed ${tool.count} tasks`}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Suggested Actions */}
                  {msg.suggested_actions && msg.suggested_actions.length > 0 && (
                    <div className="suggested-actions">
                      <div className="suggest-header">
                        <span className="suggest-icon">💡</span>
                        <span className="suggest-title">Try:</span>
                      </div>
                      <div className="suggest-buttons">
                        {msg.suggested_actions.map((action, idx) => (
                          <button
                            key={idx}
                            className="suggest-btn"
                            onClick={() => sendMessage(action)}
                          >
                            {action}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="message-wrapper ai">
                <div className="message-bubble">
                  <div className="thinking">
                    <span className="thinking-dots">...</span>
                    Gemini AI is thinking
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="input-area">
            <form onSubmit={handleSubmit}>
              <div className="input-container">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  className="message-input"
                  disabled={loading}
                />
                <button 
                  type="submit" 
                  className="send-button"
                  disabled={loading || !input.trim()}
                >
                  {loading ? 'Sending...' : 'Send'}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Sidebar - Quick Actions */}
        <div className="sidebar">
          <div className="sidebar-section">
            <h3>🚀 Quick Actions</h3>
            <div className="quick-actions-grid">
              {quickActions.map((action, idx) => (
                <button
                  key={idx}
                  className="quick-action-btn"
                  onClick={() => sendMessage(action.text)}
                >
                  <span className="action-emoji">{action.emoji}</span>
                  <span className="action-text">{action.text}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="sidebar-section">
            <h3>📚 Examples</h3>
            <ul className="examples-list">
              <li>"Add task to complete project"</li>
              <li>"Show me pending tasks"</li>
              <li>"Mark task 3 as complete"</li>
              <li>"Delete the shopping task"</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          <strong>AI Todo Chatbot</strong> • 
          Built with FastAPI + Gemini AI + React
        </p>
      </footer>
    </div>
  );
}

export default App;