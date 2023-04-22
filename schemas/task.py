from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str


class TaskUpdate(TaskBase):
    completed: bool = False


class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
