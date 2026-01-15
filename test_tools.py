#!/usr/bin/env python3
"""
Test all MCP tools - Updated with model_dump()
"""
import asyncio
import json
from mcp_server.tools import (
    add_task, list_tasks, complete_task, 
    delete_task, update_task
)
from mcp_server.schemas import (
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest,
    DeleteTaskRequest, UpdateTaskRequest
)

async def test_all_tools():
    print("🧪 Testing MCP Tools...")
    print("=" * 50)
    
    user_id = "test_user_001"
    
    # Test 1: Add Task
    print("\n1️⃣ Testing ADD_TASK...")
    add_req = AddTaskRequest(
        user_id=user_id,
        title="Buy groceries",
        description="Milk, eggs, bread"
    )
    result = await add_task(add_req)
    print(f"   Result: {result.model_dump()}")
    
    task_id = result.task_id
    
    # Test 2: List Tasks
    print("\n2️⃣ Testing LIST_TASKS...")
    list_req = ListTasksRequest(user_id=user_id, status="all")
    result = await list_tasks(list_req)
    print(f"   Found {result.count} tasks")
    for task in result.tasks[:3]:  # Show first 3
        print(f"   - Task {task.id}: {task.title} (Completed: {task.completed})")
    
    # Test 3: Complete Task
    print("\n3️⃣ Testing COMPLETE_TASK...")
    if task_id > 0:
        complete_req = CompleteTaskRequest(user_id=user_id, task_id=task_id)
        result = await complete_task(complete_req)
        print(f"   Result: {result.model_dump()}")
    
    # Test 4: Update Task
    print("\n4️⃣ Testing UPDATE_TASK...")
    if task_id > 0:
        update_req = UpdateTaskRequest(
            user_id=user_id,
            task_id=task_id,
            title="Buy groceries and fruits",
            description="Milk, eggs, bread, apples, bananas"
        )
        result = await update_task(update_req)
        print(f"   Result: {result.model_dump()}")
    
    # Test 5: List Tasks again
    print("\n5️⃣ Testing LIST_TASKS (after updates)...")
    result = await list_tasks(list_req)
    print(f"   Found {result.count} tasks")
    for task in result.tasks:
        print(f"   - Task {task.id}: {task.title} (Completed: {task.completed})")
    
    # Test 6: Delete Task
    print("\n6️⃣ Testing DELETE_TASK...")
    if task_id > 0:
        delete_req = DeleteTaskRequest(user_id=user_id, task_id=task_id)
        result = await delete_task(delete_req)
        print(f"   Result: {result.model_dump()}")
    
    print("\n" + "=" * 50)
    print("✅ All tools tested successfully!")

if __name__ == "__main__":
    asyncio.run(test_all_tools())