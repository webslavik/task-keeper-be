from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.task import TaskBase, TaskUpdate
from src.db_setup import get_db

from src.repositories.task import TaskRepository
from src.utils import check_authentication, get_current_user


router = APIRouter(tags=["Tasks"], prefix="/api/tasks")


@router.get("/", dependencies=[Depends(check_authentication)])
def get_tasks(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tasks = TaskRepository.get_tasks(db, current_user.id)

    return {"tasks": tasks}


@router.post("/", dependencies=[Depends(check_authentication)], status_code=status.HTTP_201_CREATED)
def create_task(task: TaskBase, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    created_task = TaskRepository.create_task(db, task, current_user.id)

    return {"task": created_task}


@router.get("/{task_id}", dependencies=[Depends(check_authentication)])
def get_task(task_id: int, db: Session = Depends(get_db)):
    found_task = TaskRepository.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return {"task": found_task}


@router.patch("/{task_id}", dependencies=[Depends(check_authentication)])
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    found_task = TaskRepository.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = TaskRepository.update_task(db, task_id, task=task)

    return {"task": updated_task}


@router.delete("/{task_id}", dependencies=[Depends(check_authentication)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    found_task = TaskRepository.get_task(db, task_id)

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    TaskRepository.delete_task(db, task_id)

    return {"message": "Task was deleted"}
