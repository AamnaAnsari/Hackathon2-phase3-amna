# Database Schema Specification

## Overview
This project uses **Neon Serverless PostgreSQL** with **SQLModel (SQLAlchemy + Pydantic)** as the ORM. The schema is designed for multi-user isolation.

---

## 1. Users Table (Managed by Better Auth)
Stores user credentials and profile information.

| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | String | Primary Key | Unique User ID (from Better Auth) |
| `email` | String | Unique, Not Null | User's login email |
| `name` | String | Nullable | User's display name |
| `created_at` | DateTime | Default: Now | Account creation timestamp |

---

## 2. Tasks Table
Stores individual todo items for each user.

| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto-inc | Unique task identifier |
| `user_id` | String | Foreign Key (users.id) | **Owner of the task (Security Link)** |
| `title` | String | Not Null (1-200 chars) | Task heading |
| `description` | Text | Nullable | Detailed notes |
| `completed` | Boolean | Default: False | Status of the task |
| `created_at` | DateTime | Default: Now | Creation timestamp |
| `updated_at` | DateTime | On Update: Now | Last modification timestamp |

---

## 3. Relationships & Security
- **One-to-Many:** One User can have multiple Tasks.
- **Row Level Logic:** Every API query must filter by `user_id` to ensure Aamna cannot see Bilal's tasks.
- **Indexing:** Index on `tasks.user_id` for faster searching.

# Phase 3 : 
## AI Todo Chatbot Core

This document defines the technical requirements for the **FastAPI backend** of the AI Todo Chatbot, built using the **Agentic Dev Stack** workflow.

The backend follows a **stateless architecture**, acting as middleware that orchestrates interactions between the **ChatKit UI**, **OpenAI Agents SDK**, and the **MCP (Model Context Protocol) Server**.

---

## 1. System Architecture

The backend operates as a **stateless middleware**.  
Each incoming request must contain sufficient context (`user_id`, `conversation_id`) to fully reconstruct the agent’s memory from the database.

### Architecture Layers

- **Communication Layer**  
  FastAPI handles all HTTP request and response handling.

- **Orchestration Layer**  
  OpenAI Agents SDK manages the agent execution loop, reasoning, and tool-calling logic.

- **Tool Layer**  
  Official MCP SDK exposes task-related operations as tools for the agent.

- **Persistence Layer**  
  Neon Serverless PostgreSQL stores tasks, conversations, and message logs.

---

## 2. Technical Stack

- **Framework**: FastAPI (Python 3.9+)
- **Agent SDK**: OpenAI Agents SDK (with Gemini AI integration)
- **Protocol**: Official MCP SDK
- **ORM**: SQLModel (Pydantic-based validation + SQL operations)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (integrated via FastAPI dependencies)

---

## 3. Database Schema (Neon PostgreSQL)

To maintain stateless execution, the database persists the **complete conversation state**.

### Task Model

| Field        | Type          | Description                              |
|-------------|---------------|------------------------------------------|
| id          | Integer (PK)  | Unique task identifier                   |
| user_id     | String        | Owner of the task (Indexed)              |
| title       | String        | Task title (Max 255 characters)          |
| description | Text          | Optional task details                    |
| completed   | Boolean       | Completion status (Default: `false`)     |
| created_at  | Timestamp     | Auto-generated creation time             |

### Conversation Model

- Tracks a `conversation_id` associated with a `user_id`
- Represents a single chat session

### Message Model

- Stores message `role` (`user`, `assistant`, `tool`)
- Stores message `content`
- Linked to a `conversation_id` to rebuild ChatKit history

---

## 4. API Endpoints

### `POST /api/{user_id}/chat`

Primary interface for interacting with the AI Agent.

#### Stateless Execution Flow

1. **Request Reception**  
   Receives the user message and `conversation_id`.

2. **History Reconstruction**  
   Fetches all messages linked to the `conversation_id` from Neon DB.

3. **Agent Initialization**  
   Initializes the OpenAI Agent with:
   - System prompt
   - Available MCP tools
   - Reconstructed conversation history

4. **Runner Loop**
   - Agent analyzes user intent (Add, List, Complete, Update, Delete).
   - Agent invokes MCP tools when required.

5. **Persistence**
   - Saves user message
   - Saves tool outputs
   - Saves final assistant response

6. **Response**
   Returns a JSON payload containing:
   - Assistant response
   - Tool-call metadata (if any)

---

## 5. MCP Tool Implementation

The MCP Server provides a **stateless interface** for database operations.

### Available Tools

- `add_task(user_id, title, description)`  
  Inserts a new task.

- `list_tasks(user_id, status)`  
  Returns tasks filtered by `pending`, `completed`, or `all`.

- `complete_task(user_id, task_id)`  
  Marks a task as completed.

- `delete_task(user_id, task_id)`  
  Deletes a task permanently.

- `update_task(user_id, task_id, title, description)`  
  Updates task fields.

---

## 6. Security and Error Handling

- **Ownership Verification**  
  Every tool validates that the `task_id` belongs to the provided `user_id`.

- **Error Mapping**  
  Standardized error codes are returned to the agent:
  - `TASK_NOT_FOUND`
  - `VALIDATION_ERROR`
  - `UNAUTHORIZED_ACTION`

- **Rate Limiting**  
  Applied at the FastAPI level to prevent API abuse.

---

## 7. Performance Targets

- **Processing Time**  
  Intent recognition and tool selection must complete within **< 3 seconds**.

- **Database Performance**
  - Composite indexes on `user_id` and `created_at`
  - Optimized queries for fast conversation reconstruction
