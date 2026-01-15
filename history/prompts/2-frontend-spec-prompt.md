# 📜 Todo App Project 

**ID:** 1  
**Title:** frontend_spec_prompt
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
**Files:** frontend_spec.md  
**Tests:** Not Required  

---

# 🧠 Frontend Initialization Prompt:

You are an **AI Frontend Engineer Agent** tasked with initializing the **Todo AI Chatbot frontend**.  
All actions must strictly follow the **frontend_spec.md** and the **Agentic Dev Stack workflow**.

You do **not** maintain memory internally.  
All state must be reconstructed from the backend for stateless UI behavior.

---

## 📌 Project Context

- **Frontend Framework:** React 18.2  
- **UI Library:** OpenAI ChatKit (for conversation components)  
- **State Management:** React Context / Hooks (stateless)  
- **API Client:** Axios or Fetch API  
- **Styling:** Tailwind CSS (WCAG 2.1 AA compliant, fully responsive)  
- **Backend Endpoint:** POST `/api/{user_id}/chat`  
- **Directory Structure:** `/frontend`  

---

## 🎯 Core Responsibilities

- Setup a clean React project structure in `/frontend`  
- Implement **ChatWindow** component integrated with OpenAI ChatKit  
- Render **MessageList** with historical messages fetched from the backend  
- Implement **InputArea** with real-time typing indicators  
- Ensure **stateless UI behavior**: fetch conversation history on mount  
- Implement Axios API service to communicate with backend  
- Handle errors gracefully with user-friendly error messages  

---

## 🏗️ Agentic Dev Stack Workflow

Follow this workflow **strictly**:

1. **Specification Phase**
   - Read and internalize FRONTEND_SPEC.md  
   - Identify components, API needs, and styling rules

2. **Planning Phase**
   - Break the initialization into clear, incremental tasks  
   - Prioritize tasks for minimal dependencies

3. **Task Breakdown**

- **Task 1:** Initialize React project in `/frontend`  
- **Task 2:** Install dependencies (React, Tailwind CSS, Axios, OpenAI ChatKit)  
- **Task 3:** Setup global layout (responsive, WCAG-compliant)  
- **Task 4:** Implement `ChatWindow` component  
- **Task 5:** Implement `MessageList` to render historical messages  
- **Task 6:** Implement `InputArea` with real-time typing indicators  
- **Task 7:** Setup Axios API service for POST `/api/{user_id}/chat`  
- **Task 8:** Implement error boundaries for friendly messages  
- **Task 9:** Apply Tailwind CSS styling and design tokens  
- **Task 10:** Test responsiveness across Mobile, Tablet, Desktop  

4. **Execution Phase**
   - Execute tasks sequentially or in parallel where safe  
   - Ensure each component is stateless and integrates fully with the backend  

5. **Validation Phase**
   - Verify UI renders historical messages correctly  
   - Test real-time typing indicator functionality  
   - Confirm API calls are successful and errors are handled gracefully  
   - Validate accessibility compliance and responsive design  

---

## 🛠️ Constraints

- **Stateless UI:** No client-side memory beyond context reconstruction  
- **Accessibility:** WCAG 2.1 AA standard  
- **Responsiveness:** Mobile, Tablet, Desktop  
- **Error Handling:** Friendly, non-technical messages  
- **Design Consistency:** Tailwind CSS, minimal “Productivity” theme  
- **Security:** No sensitive data exposure in the frontend  

---

## ✅ Output Expectations

- Clean React project scaffold in `/frontend`  
- Stateless, responsive, accessible UI  
- Working Axios API integration with backend endpoint  
- Clear and maintainable code adhering to Agentic Dev Stack principles  
