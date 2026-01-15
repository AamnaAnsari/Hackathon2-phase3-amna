import asyncio
from mcp import Client
from mcp_client.stdio import stdio_client

async def test_tools():
    async with stdio_client(["python", "run_mcp.py"]) as (read, write):
        async with Client(read, write) as client:
            # Initialize
            await client.initialize()
            
            # Test add_task
            result = await client.call_tool(
                "add_task_tool",
                {"user_id": "test_user", "title": "Buy groceries"}
            )
            print("Add Task Result:", result)
            
            # Test list_tasks
            result = await client.call_tool(
                "list_tasks_tool",
                {"user_id": "test_user", "status": "all"}
            )
            print("List Tasks Result:", result)

if __name__ == "__main__":
    asyncio.run(test_tools())