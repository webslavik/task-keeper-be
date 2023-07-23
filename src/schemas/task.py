from datetime import datetime
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str


class TaskUpdate(TaskBase):
    completed: bool = False


class TaskCreate(TaskBase):
    user_id: int


class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class TasksResponseSchema(BaseModel):
    tasks: list[Task]
