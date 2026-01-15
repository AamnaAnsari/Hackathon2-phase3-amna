# 📜 Todo App Project 

**ID:** 3
**Title:** agent_spec_prompt
**Stage:** Plan  
**Date:** 2026-01-16
**Surface:** Full-Stack  
**Model:** Claude Code  
**Feature:** Agentic Development Stack  
**Branch:** main  
**User:** @user  
**Command:** /sp.plan  
**Labels:** Core, Security, Workflow  
**Links:** N/A  
**Files:** agent_spec.md  
**Tests:** Not Required  

---

# 🤖 AI Agent Implementation Prompt:

You are an **AI Backend Engineer Agent** tasked with implementing the **Todo AI Chatbot Agent**.  
All logic must strictly follow **agent_spec.md** and the **Agentic Dev Stack workflow**.  

You do **not** maintain memory internally. All state is reconstructed from the backend database for stateless operation.

---

## 📌 Project Context

- **Core SDK:** OpenAI Agents SDK  
- **Tool Integration:** MCP Server tools (`add_task`, `list_tasks`, `complete_task`, `update_task`)  
- **Context Source:** Neon Database (conversation history)  
- **Response Generation:** Templates defined in AGENT_SPEC.md  
- **Model:** Google Gemini AI  

---

## 🎯 Core Responsibilities

- Implement an Agent capable of:
  - **Intent classification** (ADD_TASK, LIST_TASKS, COMPLETE_TASK, UPDATE_TASK)  
  - **Entity extraction** (task_id, title, due_date, status)  
  - **Context injection** from historical messages  
- Integrate with MCP tools for all persistent operations  
- Generate **natural language responses** using structured success/error templates  
- Handle ambiguity by prompting users for missing parameters  
- Ensure stateless, secure, and reproducible behavior  

---

## 🏗️ Agentic Dev Stack Workflow

Follow this workflow **strictly**:

1. **Specification Phase**
   - Read and internalize agent_spec.md  
   - Understand required intents, entity parameters, decision logic, and response templates  

2. **Planning Phase**
   - Break down the agent implementation into incremental, independent tasks  
   - Prioritize tasks to minimize dependencies and simplify testing  

3. **Implementation Tasks**

- **Task 1:** Initialize Agent instance using OpenAI Agents SDK with Google Gemini AI  
- **Task 2:** Implement **Input Processor** for text normalization  
- **Task 3:** Implement **Intent Classifier** with confidence thresholds (0.7–0.9)  
- **Task 4:** Implement **Entity Extractor** to capture task_id, title, due_date  
- **Task 5:** Implement **Context Manager** to fetch and inject historical messages  
- **Task 6:** Implement **Tool Orchestrator** for MCP tool calls based on detected intent  
- **Task 7:** Implement **Response Generator** to return structured messages using templates  
- **Task 8:** Handle missing parameters and ambiguity prompts  
- **Task 9:** Integrate logging and error handling for debugging and reliability  
- **Task 10:** Write unit tests for intent recognition, entity extraction, and tool orchestration  

4. **Execution Phase**
   - Implement tasks sequentially, ensuring stateless operation  
   - Validate each component individually, then test full Agent workflow  

5. **Validation Phase**
   - Confirm Agent executes correct MCP tool for each intent  
   - Validate responses match templates for success, error, and clarification  
   - Test handling of missing or ambiguous inputs  
   - Ensure total processing time < 3 seconds  
   - Verify >90% intent recognition and >85% entity extraction accuracy  

---

## 🛠️ Constraints

- **Statelessness:** No internal memory; rely solely on historical messages per request  
- **Security:** All tool calls scoped to the correct `user_id`  
- **Accuracy:** Use high-confidence thresholds before executing actions  
- **Reproducibility:** Same input → same output consistently  
- **Error Handling:** Friendly, human-readable messages without exposing internal details  

---

## ✅ Output Expectations

- Fully functional Agent integrated with MCP tools  
- Stateless, context-aware, and responsive to user inputs  
- Correct application of intent recognition and entity extraction  
- Natural language responses consistent with AGENT_SPEC.md templates  
- Robust handling of missing parameters and ambiguous inputs  
- Code organized, maintainable, and ready for backend deployment  
