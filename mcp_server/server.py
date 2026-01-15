import asyncio
import json
from typing import Dict, Any
import logging

from mcp.server import Server
from mcp.shared.exceptions import McpError
import mcp.server.stdio

from .tools import (
    add_task, list_tasks, complete_task,
    delete_task, update_task
)
from .schemas import (
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest,
    DeleteTaskRequest, UpdateTaskRequest
)
from .database import create_db_and_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TodoMCPServer:
    def __init__(self, server_name: str = "todo-mcp-server"):
        self.server = Server(server_name)
        self.setup_tools()
        logger.info(f"MCP Server '{server_name}' initialized")
    
    def setup_tools(self):
        """Register all MCP tools"""
        
        @self.server.list_tools()
        async def handle_list_tools():
            return [
                {
                    "name": "add_task",
                    "description": "Add a new task to the todo list",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description"}
                        },
                        "required": ["user_id", "title"]
                    }
                },
                {
                    "name": "list_tasks",
                    "description": "List tasks with optional status filter",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "status": {
                                "type": "string",
                                "description": "Task status filter",
                                "enum": ["all", "pending", "completed"],
                                "default": "all"
                            }
                        },
                        "required": ["user_id"]
                    }
                },
                {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "integer", "description": "Task ID to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                },
                {
                    "name": "delete_task",
                    "description": "Delete a task from the list",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "integer", "description": "Task ID to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                },
                {
                    "name": "update_task",
                    "description": "Update task title or description",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "integer", "description": "Task ID to update"},
                            "title": {"type": "string", "description": "New task title"},
                            "description": {"type": "string", "description": "New task description"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]):
            logger.info(f"Tool called: {name} with args: {arguments}")
            
            try:
                if name == "add_task":
                    request = AddTaskRequest(**arguments)
                    result = await add_task(request)
                    return [{"type": "text", "text": json.dumps(result.model_dump())}]
                
                elif name == "list_tasks":
                    request = ListTasksRequest(**arguments)
                    result = await list_tasks(request)
                    return [{"type": "text", "text": json.dumps(result.model_dump(), default=str)}]
                
                elif name == "complete_task":
                    request = CompleteTaskRequest(**arguments)
                    result = await complete_task(request)
                    return [{"type": "text", "text": json.dumps(result.model_dump())}]
                
                elif name == "delete_task":
                    request = DeleteTaskRequest(**arguments)
                    result = await delete_task(request)
                    return [{"type": "text", "text": json.dumps(result.model_dump())}]
                
                elif name == "update_task":
                    request = UpdateTaskRequest(**arguments)
                    result = await update_task(request)
                    return [{"type": "text", "text": json.dumps(result.model_dump())}]
                
                else:
                    raise McpError(f"Unknown tool: {name}")
                    
            except Exception as e:
                logger.error(f"Tool error: {e}")
                return [{
                    "type": "text",
                    "text": json.dumps({
                        "error": str(e),
                        "status": "error"
                    })
                }]
    
    async def run_stdio(self):
        """Run MCP server with stdio transport"""
        try:
            create_db_and_tables()
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise
        
        logger.info("Starting MCP server (stdio mode)...")
        
        # MCP 1.24.0 with anyio 3.7.1 compatible code
        async with mcp.server.stdio.stdio_server() as streams:
            read_stream, write_stream = streams
            await self.server.run(
                read_stream,
                write_stream,
                {"protocolVersion": "2024-11-05", "capabilities": {}}
            )

async def main_async():
    server = TodoMCPServer()
    await server.run_stdio()

def main():
    """Main entry point"""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    main()