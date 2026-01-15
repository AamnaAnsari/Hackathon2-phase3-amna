#  CLAUDE.md: Agent Instructions

## 🛠️ Project Identity
You are an AI developer implementing the **Todo AI Chatbot** (Phase III).  
Your goal is to build a stateless, MCP-based task manager using the **Agentic Dev Stack** workflow[cite: 3].

##  Core Directives
- **No Manual Coding**: You must generate a plan and break it into tasks before implementation[cite: 3].  
- **Statelessness**: Never store session data in memory. [cite_start]Always reconstruct context from the Neon Database[cite: 3, 11].  
- [cite_start]**Protocol Compliance**: Use the **Official MCP SDK** for tools and **OpenAI Agents SDK** for logic[cite: 3, 40].  
- [cite_start]**Security**: Verify `user_id` ownership for every database operation (CRUD)[cite: 41, 59].

## 📂 Key Technical References
- [cite_start]**Backend**: FastAPI + SQLModel + Neon PostgreSQL[cite: 1, 3].  
- [cite_start]**AI**: Google Gemini AI (integrated via OpenAI Agents SDK)[cite: 8, 20].  
- [cite_start]**Frontend**: React + OpenAI ChatKit[cite: 3].  
- **Specifications**: Refer to `/specs/backend_spec.md` and `/specs/mcp_spec.md` for tool schemas.

## 🔧 Build & Test Commands
- [cite_start]**Install Backend**: `pip install -r requirements.txt`[cite: 4].  
- [cite_start]**Run Backend**: `uvicorn backend.main:app --reload`[cite: 4].  
- [cite_start]**Install Frontend**: `cd frontend && npm install`[cite: 4].  
- **Test Suite**: `pytest` (Backend) | [cite_start]`npm test` (Frontend)[cite: 5].

## 📝 Coding Style
- [cite_start]Use **Type Hints** for all Python functions[cite: 12].  
- [cite_start]Implement **SQLModel** for all DB interactions to ensure Pydantic validation[cite: 3, 12].  
- [cite_start]Return structured JSON errors using the codes defined in `mcp_spec.md`[cite: 57, 58].
