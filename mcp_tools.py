"""
Wrapper for MCP tools to integrate with FastAPI
"""
import asyncio
from typing import Dict, Any
import logging

from mcp_server.tools import (
    add_task, list_tasks, complete_task,
    delete_task, update_task
)
from mcp_server.schemas import (
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest,
    DeleteTaskRequest, UpdateTaskRequest
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TodoTools:
    """Wrapper for MCP todo tools"""
    
    @staticmethod
    async def add_task_tool(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """Add a new task"""
        request = AddTaskRequest(
            user_id=user_id,
            title=title,
            description=description
        )
        result = await add_task(request)
        return result.model_dump()
    
    @staticmethod
    async def list_tasks_tool(user_id: str, status: str = "all") -> Dict[str, Any]:
        """List tasks with filter"""
        request = ListTasksRequest(user_id=user_id, status=status)
        result = await list_tasks(request)
        return result.model_dump()
    
    @staticmethod
    async def complete_task_tool(user_id: str, task_id: int) -> Dict[str, Any]:
        """Mark task as complete"""
        request = CompleteTaskRequest(user_id=user_id, task_id=task_id)
        result = await complete_task(request)
        return result.model_dump()
    
    @staticmethod
    async def delete_task_tool(user_id: str, task_id: int) -> Dict[str, Any]:
        """Delete a task"""
        request = DeleteTaskRequest(user_id=user_id, task_id=task_id)
        result = await delete_task(request)
        return result.model_dump()
    
    @staticmethod
    async def update_task_tool(user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Update task"""
        request = UpdateTaskRequest(
            user_id=user_id,
            task_id=task_id,
            title=title,
            description=description
        )
        result = await update_task(request)
        return result.model_dump()

# Global instance
todo_tools = TodoTools()