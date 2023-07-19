from datetime import datetime
from pydantic import BaseModel, EmailStr

from src.schemas.task import Task


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserBase):
    first_name: str
    last_name: str


class UserLogin(UserBase):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime
    tasks: list[Task]

    class Config:
        orm_model = True
