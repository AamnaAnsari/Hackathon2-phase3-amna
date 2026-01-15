"""
Pydantic Schemas for Request/Response
Updated for Pydantic v2
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# ========== REQUEST SCHEMAS ==========

class AddTaskRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None

class ListTasksRequest(BaseModel):
    user_id: str
    status: str = "all"  # "all", "pending", "completed"

class CompleteTaskRequest(BaseModel):
    user_id: str
    task_id: int

class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: int

class UpdateTaskRequest(BaseModel):
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None

# ========== RESPONSE SCHEMAS ==========

class TaskResponse(BaseModel):
    task_id: int
    status: str  # "created", "completed", "deleted", "updated", "error"
    title: str

class TaskDetail(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

class ListTasksResponse(BaseModel):
    tasks: List[TaskDetail]
    count: int