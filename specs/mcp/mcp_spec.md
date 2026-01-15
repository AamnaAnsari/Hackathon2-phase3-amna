# 🛠️ MCP_SPEC.md:

This specification defines the **Model Context Protocol (MCP) server architecture** for the **Todo AI Chatbot**.  
It standardizes **tools, schemas, and database interactions** that allow the AI Agent to perform task management operations.

---

## 1. MCP Architecture Overview

The MCP server acts as a **tool-based service layer** between the **OpenAI Agents SDK** and the **Neon PostgreSQL database**.

### Core Components

- **Tool Registry:** Central catalog of all task management functions.  
- **Request Handler:** Validates incoming tool calls against predefined JSON schemas.  
- **Database Connector:** Executes **stateless SQL operations** via SQLModel.  
- **Error Handler:** Maps database exceptions to **standardized MCP error codes**.

---

## 2. Tool Definitions & Schemas

All tools are implemented using the **Official MCP SDK** with strict parameter validation.

### Tool: `add_task`

- **Purpose:** Creates a new todo item in the database.  
- **Parameters:**  
  - `user_id` (string, required) — Unique identifier for the user  
  - `title` (string, required) — Title of the task  
  - `description` (string, optional) — Detailed notes  
- **Returns:** `task_id`, `status`, `title`

### Tool: `list_tasks`

- **Purpose:** Retrieves tasks with optional filtering  
- **Parameters:**  
  - `user_id` (string, required)  
  - `status` (string, optional) — Filters by `all`, `pending`, or `completed`  
- **Returns:** Array of task objects

### Tool: `complete_task`

- **Purpose:** Marks a specific task as finished  
- **Parameters:**  
  - `user_id` (string, required)  
  - `task_id` (integer, required)  
- **Returns:** Confirmation of completion and a timestamp

### Tool: `update_task`

- **Purpose:** Modifies the title or description of an existing task  
- **Parameters:**  
  - `user_id`  
  - `task_id`  
  - At least one optional field: `title` or `description`  

---

## 3. Database & Persistence Layer

To ensure **statelessness**, every tool call interacts **directly** with the Neon Serverless PostgreSQL database.

```sql
-- Core Tasks Table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
## 4. Error Handling & Security
Ownership Check

Tools must verify that the task_id belongs to the user_id before execution.

## Standardized Errors:

VALIDATION_ERROR: Invalid input parameters

TASK_NOT_FOUND: Task ID does not exist for the user

DATABASE_ERROR: Connection or query failure

## Stateless Operation:

No session state is held within the MCP server

All state is persisted to the database