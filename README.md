# 🚀 AI Todo Chatbot (Phase III)

## 📖 Overview
An AI-powered task management system that uses natural language to perform CRUD operations.  
Built on **Model Context Protocol (MCP)** architecture, it features a stateless backend and a real-time conversational UI[cite: 2, 3].

## ✨ Key Features
- **Natural Language Processing**: Understands intents like "Add a task to buy groceries" or "What's pending?"[cite: 3, 22].  
- **Stateless Architecture**: Conversation history and task states are persisted in **Neon PostgreSQL**[cite: 3, 54].  
- [cite_start]**MCP Server**: 5 standardized tools (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`) exposed via the Official MCP SDK[cite: 3, 40].  
- **ChatKit UI**: A premium, responsive chat interface designed with OpenAI ChatKit.  

## 🏗️ Architecture
[cite_start]The system follows the **Agentic Dev Stack** workflow:

1. **Frontend**: React UI using ChatKit[cite: 3].  
2. [cite_start]**Backend**: FastAPI server running OpenAI Agents SDK[cite: 3].  
3. [cite_start]**Intelligence**: Gemini AI for intent recognition and entity extraction[cite: 8, 20, 21].  
4. [cite_start]**Tools**: MCP Server for direct database interaction[cite: 3, 40].  
5. [cite_start]**Storage**: Neon Serverless PostgreSQL[cite: 3, 53].  

## 🚀 Quick Start

### Prerequisites
- Python 3.9+  
- Node.js 16+  
- Neon PostgreSQL Account  
- Gemini API Key  

### Installation & Setup

#### Backend Configuration
```bash

cp .env.example .env
# Add GEMINI_API_KEY and DATABASE_URL to .env
pip install -r requirements.txt
python main.py
```

## Prepared by Aamna Ansari.