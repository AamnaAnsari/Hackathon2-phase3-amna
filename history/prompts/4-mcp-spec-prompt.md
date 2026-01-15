# 📜 Todo App Project 

**ID:** 4
**Title:** mcp_spec_prompt
**Stage:** Task 
**Date:** 2026-01-16  
**Surface:** Full-Stack  
**Model:** Claude Code  
**Feature:** Agentic Development Stack  
**Branch:** main  
**User:** @user  
**Command:** /sp.task  
**Labels:** Core, Security, Workflow  
**Links:** N/A  
**Files:** mcp_spec.md  
**Tests:** Not Required  

---

# 🤖 MCP Server Implementation Prompt

This prompt defines the task for implementing the **Model Context Protocol (MCP) Server** for the Todo AI Chatbot. 
It follows the **Agentic Dev Stack workflow**: generate a technical plan, break it into tasks, and implement.

---

## 📌 Project Context

- **Purpose:** Provide a stateless, tool-based service layer for the AI Agent to manage tasks in Neon PostgreSQL.  
- **Tools to Expose:** `add_task`, `list_tasks`, `complete_task`,  `update_task`  
- **Database:** Neon Serverless PostgreSQL  
- **ORM:** SQLModel  
- **Error Codes:** `TASK_NOT_FOUND`, `VALIDATION_ERROR`, `DATABASE_ERROR`  
- **Endpoints:** Tool RPCs, `health check`, `discovery`  

---

## 🎯 Core Requirements

1. **MCP SDK Integration**
   - Use the Official MCP SDK to define and expose all task management tools.
   - Ensure tools are callable by the AI Agent only via structured requests.

2. **Database Operations**
   - Each tool must interact directly with Neon PostgreSQL using SQLModel.
   - Support full CRUD for tasks.
   - Ensure stateless operation; no internal session state.

3. **Parameter Validation**
   - Implement strict validation of tool inputs using JSON schemas.
   - Validate all required fields and enforce correct types.

4. **Security & Ownership**
   - Every tool must verify that the `task_id` belongs to the requesting `user_id`.
   - Deny operations on tasks that do not belong to the user.

5. **Error Handling**
   - Return standardized error codes when issues occur:
     - `TASK_NOT_FOUND` — Task ID does not exist for this user  
     - `VALIDATION_ERROR` — Input parameters invalid  
     - `DATABASE_ERROR` — Query or connection failure

6. **Utility Endpoints**
   - `health check` — Verify the MCP server is running  
   - `discovery` — List available tools and their input/output schemas

---

## 🛠️ Implementation Guidelines

- Follow **stateless, reproducible execution** principles.
- Use **Agentic Dev Stack workflow**:
  1. Generate a technical plan for the MCP server.
  2. Break the plan into implementable tasks per tool.
  3. Implement one tool at a time, testing validation, security, and database interactions.
- Include **logging and error messages** for debugging and monitoring.
- Ensure **consistent responses** matching the MCP specification for all tools.

---

## ✅ Success Criteria

- All tools work correctly and securely for multiple users.
- Ownership validation prevents cross-user access.
- API responses follow MCP error codes and schemas.
- `health check` and `discovery` endpoints respond correctly.
- The MCP server is fully stateless and ready to integrate with the AI Agent.

---
