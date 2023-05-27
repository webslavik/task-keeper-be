from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.task import TaskBase, TaskUpdate
from src.db_setup import get_db
from src.crud.task import read_task, create_task, update_task, delete_task
from src.crud.user import get_user_by_id

from src.utils import check_authentication_token


router = APIRouter()


@router.get("/users/{user_id}/tasks", dependencies=[Depends(check_authentication_token)])
def get_tasks(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"tasks": user.tasks}


@router.get("/users/{user_id}/tasks/{task_id}")
def get_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_task = read_task(db, task_id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return {"task": db_task}


@router.post("/users/{user_id}/tasks", dependencies=[Depends(check_authentication_token)], status_code=status.HTTP_201_CREATED)
def add_task(user_id: int, task: TaskBase, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_task = create_task(db, task=task, user_id=user_id)

    return {"task": new_task}


@router.patch("/users/{user_id}/tasks/{task_id}")
def change_task(user_id: int, task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_task = read_task(db, id=task_id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = update_task(db, id=task_id, task=task)

    return {"task": updated_task}


@router.delete("/users/{user_id}/tasks/{task_id}")
def remove_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_task = read_task(db, id=task_id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    delete_task(db, id=task_id)

    return {"message": "Task was deleted"}
