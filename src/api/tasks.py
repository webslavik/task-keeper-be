from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.task import TaskBase, TaskUpdate, Task
from src.db_setup import get_db
from src.crud.task import read_tasks, read_task, create_task, update_task, delete_task


router = APIRouter()

@router.get("/tasks", response_model=List[Task])
def get_tasks(db: Session = Depends(get_db)):
    return read_tasks(db)


@router.get("/tasks/{id}", response_model=Task)
def get_task(id: int, db: Session = Depends(get_db)):
    db_task = read_task(db, id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return db_task


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def add_task(task: TaskBase, db: Session = Depends(get_db)):
    db_task = create_task(db, task=task)

    return db_task


@router.patch("/task/{id}")
def change_task(id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = read_task(db, id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = update_task(db, id, task=task)

    return updated_task


@router.delete("/task/{id}")
def remove_task(id: int, db: Session = Depends(get_db)):
    db_task = read_task(db, id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    delete_task(db, id)

    return {"message": "Task was deleted"}
