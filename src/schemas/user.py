from datetime import datetime
from pydantic import EmailStr

from pydantic.main import BaseModel
from src.schemas.task import Task


class UserBase(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserBase):
    pass


class User(UserBase):
    id: int
    tasks: list[Task]

    class Config:
        orm_model = True


class UserLoginSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime


class UserLoginResponseSchema(BaseModel):
    access_token: str
    user: UserLoginSchema
