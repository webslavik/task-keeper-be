from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.task import TaskBase, TaskUpdate
from src.db_setup import get_db


from src.services.task import TaskService
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

    found_task = TaskService.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return {"task": found_task}


@router.post("/users/{user_id}/tasks", dependencies=[Depends(check_authentication_token)], status_code=status.HTTP_201_CREATED)
def create_task(user_id: int, task: TaskBase, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # copied_task = task.copy()
    # copied_task.user_id = user_id
    created_task = TaskService.create_task(db, task, user_id)

    return {"task": created_task}


@router.patch("/users/{user_id}/tasks/{task_id}")
def update_task(user_id: int, task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    found_task = TaskService.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = TaskService.update_task(db, task_id, task=task)

    return {"task": updated_task}


@router.delete("/users/{user_id}/tasks/{task_id}")
def delete_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    found_task = TaskService.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    TaskService.delete_task(db, task_id)

    return {"message": "Task was deleted"}
