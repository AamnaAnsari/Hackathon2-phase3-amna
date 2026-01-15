# AI Agent & Logic Specification

This document defines the **intelligence layer** of the **Todo AI Chatbot**.  
The agent acts as the **brain of the system**, converting natural language into structured actions using the **OpenAI Agents SDK** and the **Model Context Protocol (MCP)**.

---

## 1. Agent Architecture

The agent operates as a **"Thinking Middleware"**, bridging conversational input and database operations.

### Core Components

- **Input Processor**  
  Normalizes and cleanses user text for accurate analysis.

- **Intent Classifier**  
  Determines the primary goal of the user (e.g., `ADD_TASK`, `LIST_TASKS`) with **confidence thresholds** between 0.7–0.9.

- **Entity Extractor**  
  Identifies parameters such as `task_id`, `title`, or `due_date` from raw text.

- **Context Manager**  
  Reconstructs conversation state using historical messages from **Neon Database**.

- **Tool Orchestrator**  
  Selects and executes the appropriate MCP tool based on detected intent.

- **Response Generator**  
  Converts structured tool outputs into **friendly, natural language feedback** for the user.

---

## 2. Intent Recognition & Behavior Mapping

The agent uses **high-confidence thresholds** before executing any tool.  

| Primary Intent   | Natural Language Patterns                        | Associated MCP Tool |
|-----------------|-------------------------------------------------|------------------|
| ADD_TASK        | "Add...", "Create...", "I need to remember..."  | add_task          |
| LIST_TASKS      | "Show me...", "What's pending?", "List tasks"  | list_tasks        |
| COMPLETE_TASK   | "Done with...", "Mark #3 as complete", "Finished" | complete_task     |
| UPDATE_TASK     | "Update...", "Change task 1 to...", "Modify"   | update_task       |

---

## 3. Decision Logic & Tool Orchestration

The agent follows a **strict decision tree** to validate required parameters before calling an MCP tool.

- **IF ADD_TASK:**  
  Requires a `title`. If missing, prompt:  
  `"What would you like to name this task?"`

- **IF COMPLETE_TASK / DELETE_TASK:**  
  Requires a `task_id`. Agent validates the ID exists and belongs to the user.

- **IF LIST_TASKS:**  
  Optionally accepts `status_filter` (pending, completed, all). Defaults to **all** if unspecified.

---

## 4. Response Templates

To maintain a **professional and consistent personality**, the agent uses structured templates:

### Success Responses

- **Creation:** `"✅ Added '{title}' to your tasks."`  
- **Completion:** `"🎯 Task {task_id} marked as complete!"`  
- **Listing:** `"📋 Found {count} {status} tasks."`

### Error & Clarification

- **Missing Info:** `"I need more information. {missing_info}"`  
- **Not Found:** `"Task {task_id} not found in your list."`  
- **Ambiguity:** `"Did you want to add, list, or complete a task?"`

---

## 5. Performance & Accuracy Metrics

- **Response Time:** Total processing (including intent classification) must be **under 3 seconds**  
- **Recognition Accuracy:**  
  - Intent recognition target: **>90%**  
  - Entity extraction target: **>85%**

---

