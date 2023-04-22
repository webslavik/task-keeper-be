from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str


class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskUpdate(TaskBase):
    completed: bool