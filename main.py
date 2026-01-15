#!/usr/bin/env python3
"""
FastAPI Backend with Gemini AI Integration
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import logging
from datetime import datetime

# Import modules
from gemini_handler import get_gemini_assistant
from mcp_tools import todo_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Todo AI Chatbot with Gemini",
    version="2.0.0",
    description="AI-powered todo chatbot using Gemini AI and MCP tools",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "*"  # For development only
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str
    user_id: Optional[str] = None  # Can also come from path

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]
    suggested_actions: List[str]

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    ai_provider: str
    database: str
    uptime: str

# Store for conversation context (in-memory for now)
conversation_context = {}

# Startup
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Initialize Gemini (will fail if API key missing)
        gemini = get_gemini_assistant()
        logger.info("🚀 Todo AI Chatbot started with Gemini AI")
        
        # Test database connection
        from mcp_server.database import create_db_and_tables
        create_db_and_tables()
        logger.info("✅ Database initialized")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")

# Health check
@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    from datetime import datetime
    startup_time = datetime.now()
    
    return HealthResponse(
        status="healthy",
        service="Todo AI Chatbot",
        version="2.0.0",
        ai_provider="Gemini AI",
        database="NEON PostgreSQL",
        uptime=str(datetime.now() - startup_time)
    )

# Main chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint with Gemini AI integration
    
    - Processes natural language messages
    - Uses Gemini AI to understand intent
    - Executes appropriate MCP tools
    - Returns AI-generated response
    """
    user_id = request.user_id or "default_user"
    logger.info(f"💬 Chat from {user_id}: {request.message[:50]}...")
    
    try:
        # Get user context (recent tasks)
        recent_tasks = await todo_tools.list_tasks_tool(user_id, "all")
        context = {
            "recent_tasks": recent_tasks.get("tasks", [])[:3],
            "total_tasks": recent_tasks.get("count", 0)
        }
        
        # Analyze message with Gemini
        gemini = get_gemini_assistant()
        analysis = await gemini.analyze_message(request.message, context)
        
        # Execute action based on analysis
        tool_calls = []
        action_result = None
        
        if analysis["action"] != "unknown" and analysis["confidence"] > 0.6:
            action_result = await execute_action(
                user_id, 
                analysis["action"], 
                analysis["parameters"]
            )
            tool_calls = [action_result] if action_result else []
        
        # Generate response
        if analysis["confidence"] > 0.6 and "response" in analysis:
            response_text = analysis["response"]
        else:
            response_text = await gemini.generate_chat_response(request.message, analysis)
        
        # Add confirmation if action was executed
        if action_result and action_result.get("status") in ["created", "completed", "updated", "deleted"]:
            response_text += f"\n✅ Action completed: {action_result.get('title', 'Task')}"
        
        # Generate suggested actions
        suggested_actions = generate_suggestions(analysis["action"])
        
        return ChatResponse(
            conversation_id=request.conversation_id or 1,
            response=response_text,
            tool_calls=tool_calls,
            suggested_actions=suggested_actions
        )
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        return ChatResponse(
            conversation_id=request.conversation_id or 1,
            response=f"Sorry, I encountered an error: {str(e)}",
            tool_calls=[],
            suggested_actions=[]
        )

async def execute_action(user_id: str, action: str, parameters: Dict) -> Optional[Dict]:
    """Execute the appropriate action based on Gemini analysis"""
    try:
        if action == "add_task":
            result = await todo_tools.add_task_tool(
                user_id=user_id,
                title=parameters.get("title", "New Task"),
                description=parameters.get("description")
            )
            return {"tool": "add_task", **result}
        
        elif action == "list_tasks":
            result = await todo_tools.list_tasks_tool(
                user_id=user_id,
                status=parameters.get("status_filter", "all")
            )
            return {"tool": "list_tasks", **result}
        
        elif action == "complete_task":
            task_id = parameters.get("task_id")
            if task_id:
                result = await todo_tools.complete_task_tool(user_id, task_id)
                return {"tool": "complete_task", **result}
        
        elif action == "delete_task":
            task_id = parameters.get("task_id")
            if task_id:
                result = await todo_tools.delete_task_tool(user_id, task_id)
                return {"tool": "delete_task", **result}
        
        elif action == "update_task":
            task_id = parameters.get("task_id")
            if task_id:
                result = await todo_tools.update_task_tool(
                    user_id=user_id,
                    task_id=task_id,
                    title=parameters.get("title"),
                    description=parameters.get("description")
                )
                return {"tool": "update_task", **result}
        
        return None
        
    except Exception as e:
        logger.error(f"❌ Action execution error: {e}")
        return None

def generate_suggestions(current_action: str) -> List[str]:
    """Generate suggested next actions"""
    suggestions = {
        "add_task": ["List all tasks", "See pending tasks", "Add another task"],
        "list_tasks": ["Add a new task", "Mark a task complete", "See completed tasks"],
        "complete_task": ["List pending tasks", "Add another task", "Delete a task"],
        "delete_task": ["Add a new task", "List all tasks", "See what's pending"],
        "unknown": ["Add a task", "List tasks", "Mark task complete"],
        "default": ["Add task", "List tasks", "Complete task", "Delete task"]
    }
    
    return suggestions.get(current_action, suggestions["default"])

# Direct API endpoints (for testing)
@app.post("/api/tasks")
async def create_task(user_id: str, title: str, description: str = None):
    """Direct task creation"""
    return await todo_tools.add_task_tool(user_id, title, description)

@app.get("/api/tasks")
async def get_tasks(user_id: str, status: str = "all"):
    """Direct task listing"""
    return await todo_tools.list_tasks_tool(user_id, status)

@app.put("/api/tasks/{task_id}/complete")
async def complete_task_endpoint(user_id: str, task_id: int):
    """Direct task completion"""
    return await todo_tools.complete_task_tool(user_id, task_id)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Todo AI Chatbot with Gemini AI")
    print("🌐 Backend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🤖 AI Provider: Google Gemini")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )