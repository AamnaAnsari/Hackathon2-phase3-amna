
from sqlmodel import select, Session
from .models import Task
from .database import engine
from .schemas import (
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest,
    DeleteTaskRequest, UpdateTaskRequest, TaskResponse, 
    ListTasksResponse, TaskDetail
)
from typing import List
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# TOOL 1: ADD TASK
# ============================================
async def add_task(request: AddTaskRequest) -> TaskResponse:
    """
    Create a new task in the database
    
    Args:
        request: AddTaskRequest with user_id, title, description
        
    Returns:
        TaskResponse with task_id, status, title
    """
    try:
        logger.info(f"Adding task for user: {request.user_id}, title: {request.title}")
        
        # Create task object
        task = Task(
            user_id=request.user_id,
            title=request.title,
            description=request.description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save to database
        with Session(engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            
            logger.info(f"✅ Task created successfully. ID: {task.id}")
            
            return TaskResponse(
                task_id=task.id,
                status="created",
                title=task.title
            )
            
    except Exception as e:
        logger.error(f"❌ Error adding task: {e}", exc_info=True)
        return TaskResponse(
            task_id=0,
            status="error",
            title=f"Failed to create task: {str(e)}"
        )

# ============================================
# TOOL 2: LIST TASKS
# ============================================
async def list_tasks(request: ListTasksRequest) -> ListTasksResponse:
    """
    Retrieve tasks based on status filter
    
    Args:
        request: ListTasksRequest with user_id and status
        
    Returns:
        ListTasksResponse with tasks array and count
    """
    try:
        logger.info(f"Listing tasks for user: {request.user_id}, status: {request.status}")
        
        with Session(engine) as session:
            # Start with base query for user
            query = select(Task).where(Task.user_id == request.user_id)
            
            # Apply status filter if specified
            if request.status == "pending":
                query = query.where(Task.completed == False)
                logger.info("Filter: Showing pending tasks only")
            elif request.status == "completed":
                query = query.where(Task.completed == True)
                logger.info("Filter: Showing completed tasks only")
            else:  # "all"
                logger.info("Filter: Showing all tasks")
            
            # Execute query
            tasks = session.exec(query.order_by(Task.created_at.desc())).all()
            
            # Convert to response format
            task_details = [
                TaskDetail(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=task.created_at
                )
                for task in tasks
            ]
            
            logger.info(f"✅ Found {len(task_details)} tasks")
            
            return ListTasksResponse(
                tasks=task_details,
                count=len(task_details)
            )
            
    except Exception as e:
        logger.error(f"❌ Error listing tasks: {e}", exc_info=True)
        return ListTasksResponse(tasks=[], count=0)

# ============================================
# TOOL 3: COMPLETE TASK
# ============================================
async def complete_task(request: CompleteTaskRequest) -> TaskResponse:
    """
    Mark a task as completed
    
    Args:
        request: CompleteTaskRequest with user_id and task_id
        
    Returns:
        TaskResponse with task_id, status, title
    """
    try:
        logger.info(f"Completing task: user={request.user_id}, task_id={request.task_id}")
        
        with Session(engine) as session:
            # Find the task
            task = session.get(Task, request.task_id)
            
            # Check if task exists
            if not task:
                logger.warning(f"Task not found: ID {request.task_id}")
                return TaskResponse(
                    task_id=request.task_id,
                    status="error",
                    title=f"Task with ID {request.task_id} not found"
                )
            
            # Check if task belongs to user
            if task.user_id != request.user_id:
                logger.warning(f"Unauthorized access: Task {request.task_id} belongs to different user")
                return TaskResponse(
                    task_id=request.task_id,
                    status="error",
                    title=f"Task {request.task_id} does not belong to user {request.user_id}"
                )
            
            # Update task
            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            
            logger.info(f"✅ Task {task.id} marked as completed")
            
            return TaskResponse(
                task_id=task.id,
                status="completed",
                title=task.title
            )
            
    except Exception as e:
        logger.error(f"❌ Error completing task: {e}", exc_info=True)
        return TaskResponse(
            task_id=request.task_id,
            status="error",
            title=f"Failed to complete task: {str(e)}"
        )

# ============================================
# TOOL 4: DELETE TASK
# ============================================
async def delete_task(request: DeleteTaskRequest) -> TaskResponse:
    """
    Delete a task from the database
    
    Args:
        request: DeleteTaskRequest with user_id and task_id
        
    Returns:
        TaskResponse with task_id, status, title
    """
    try:
        logger.info(f"Deleting task: user={request.user_id}, task_id={request.task_id}")
        
        with Session(engine) as session:
            # Find the task
            task = session.get(Task, request.task_id)
            
            # Check if task exists
            if not task:
                logger.warning(f"Task not found: ID {request.task_id}")
                return TaskResponse(
                    task_id=request.task_id,
                    status="error",
                    title=f"Task with ID {request.task_id} not found"
                )
            
            # Check if task belongs to user
            if task.user_id != request.user_id:
                logger.warning(f"Unauthorized access: Task {request.task_id} belongs to different user")
                return TaskResponse(
                    task_id=request.task_id,
                    status="error",
                    title=f"Task {request.task_id} does not belong to user {request.user_id}"
                )
            
            # Store title before deletion for response
            task_title = task.title
            
            # Delete task
            session.delete(task)
            session.commit()
            
            logger.info(f"✅ Task {request.task_id} deleted successfully")
            
            return TaskResponse(
                task_id=request.task_id,
                status="deleted",
                title=task_title
            )
            
    except Exception as e:
        logger.error(f"❌ Error deleting task: {e}", exc_info=True)
        return TaskResponse(
            task_id=request.task_id,
            status="error",
            title=f"Failed to delete task: {str(e)}"
        )

# ============================================
# TOOL 5: UPDATE TASK
# ============================================
async def update_task(request: UpdateTaskRequest) -> TaskResponse:
    """
    Update task title or description
    
    Args:
        request: UpdateTaskRequest with user_id, task_id, title, description
        
    Returns:
        TaskResponse with task_id, status, title
    """
    try:
        logger.info(f"Updating task: user={request.user_id}, task_id={request.task_id}")
        
        with Session(engine) as session:
            # Find the task
            task = session.get(Task, request.task_id)
            
            # Check if task exists
            if not task:
                logger.warning(f"Task not found: ID {request.task_id}")
                return TaskResponse(
                    task_id=request.task_id,
                    status="error",
                    title=f"Task with ID {request.task_id} not found"
                )
            
            # Check if task belongs to user
            if task.user_id != request.user_id:
                logger.warning(f"Unauthorized access: Task {request.task_id} belongs to different user")
                return TaskResponse(
                    task_id=request.task_id,
                    status="error",
                    title=f"Task {request.task_id} does not belong to user {request.user_id}"
                )
            
            # Update fields if provided
            if request.title is not None:
                logger.info(f"Updating title from '{task.title}' to '{request.title}'")
                task.title = request.title
            
            if request.description is not None:
                logger.info(f"Updating description")
                task.description = request.description
            
            # Update timestamp
            task.updated_at = datetime.utcnow()
            
            # Save changes
            session.add(task)
            session.commit()
            session.refresh(task)
            
            logger.info(f"✅ Task {task.id} updated successfully")
            
            return TaskResponse(
                task_id=task.id,
                status="updated",
                title=task.title
            )
            
    except Exception as e:
        logger.error(f"❌ Error updating task: {e}", exc_info=True)
        return TaskResponse(
            task_id=request.task_id,
            status="error",
            title=f"Failed to update task: {str(e)}"
        )

# ============================================
# TOOL REGISTRATION
# ============================================
# Export all tools
__all__ = [
    "add_task",
    "list_tasks", 
    "complete_task",
    "delete_task",
    "update_task"
]