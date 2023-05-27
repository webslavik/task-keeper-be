from datetime import datetime
from pydantic import BaseModel, EmailStr

from src.schemas.task import Task

class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserBase):
    pass

class UserLogin(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tasks: list[Task]

    class Config:
        orm_model = True
