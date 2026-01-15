# Todo App Constitution

#  Project Constitution: AI Todo Chatbot (Updated)

---

## Article I: Project Vision

### Section 1.1: Core Purpose
To create an intelligent, conversational interface for task management that leverages **MCP architecture** and **Gemini AI** to provide a seamless natural language experience.

### Section 1.2: Guiding Principles
- **User-Centricity:** Prioritize intuitive, conversational interactions over complex UI.
- **Stateless Integrity:** Ensure the backend remains stateless by persisting all context to the database.
- **Modular Design:** Maintain a strict separation between the AI Agent, MCP tools, and Database layers.

---

## Article II: Development Standards

### Section 2.1: Python & FastAPI
- All backend code must use **Type Hints** and comply with **PEP 8** standards.
- Use **SQLModel** for unified Pydantic and SQLAlchemy operations.

### Section 2.2: AI & MCP Standards
- **Single Responsibility:** Each MCP tool must perform exactly one database operation.
- **Ownership Verification:** Tools must never modify a resource without verifying the `user_id`.
- **Graceful Failure:** AI agents must respond politely when a tool returns an error or when parameters are missing.

---

## Article III: Security & Privacy
- **Zero Persistence on Server:** No user data or chat sessions should be stored in server memory.
- **Credential Safety:** API keys (Gemini, Neon DB) must reside in `.env` files and never be committed to version control.
- **Input Sanitization:** All natural language inputs must be sanitized before processing to prevent injection.

---

## Article IV: Testing Requirements
- **Unit Testing:** Minimum 80% coverage for backend logic and MCP tool functions.
- **Integration Testing:** Successful verification of the full "Message → Agent → Tool → DB" cycle.

---

**Version**: 2.1.2 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-14

