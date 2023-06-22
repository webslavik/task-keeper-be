from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.task import TaskBase, TaskUpdate
from src.db_setup import get_db

from src.repositories.task import TaskRepository
from src.utils import check_authentication


router = APIRouter(tags=["Tasks"], prefix="/api/users")


@router.get("/{user_id:int}/tasks", dependencies=[Depends(check_authentication)])
def get_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = TaskRepository.get_tasks(db, user_id)

    return {"tasks": tasks}


@router.get("/{user_id}/tasks/{task_id}", dependencies=[Depends(check_authentication)])
def get_task(task_id: int, db: Session = Depends(get_db)):
    found_task = TaskRepository.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return {"task": found_task}


@router.post("/{user_id}/tasks", dependencies=[Depends(check_authentication)], status_code=status.HTTP_201_CREATED)
def create_task(user_id: int, task: TaskBase, db: Session = Depends(get_db)):
    created_task = TaskRepository.create_task(db, task, user_id)

    return {"task": created_task}


@router.patch("/{user_id}/tasks/{task_id}", dependencies=[Depends(check_authentication)])
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    found_task = TaskRepository.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = TaskRepository.update_task(db, task_id, task=task)

    return {"task": updated_task}


@router.delete("/{user_id}/tasks/{task_id}", dependencies=[Depends(check_authentication)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    found_task = TaskRepository.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    TaskRepository.delete_task(db, task_id)

    return {"message": "Task was deleted"}
