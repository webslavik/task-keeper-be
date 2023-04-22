from typing import List
from fastapi import APIRouter, HTTPException, status
from schemas.task import TaskBase, TaskUpdate, Task
from datetime import datetime

tasks = []

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def add_task(task: TaskBase):
    new_task = {
        "title": task.title,
        "description": task.description,
        "id": len(tasks) + 1,
        "completed": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    tasks.append(new_task)

    return new_task


@router.get("/tasks/{id}")
def get_task(id: int):
    found_task = [task for task in tasks if task["id"] == id]

    if len(found_task) is 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return found_task


@router.put("/task/{id}")
def update_task(id: int, task: TaskUpdate):
    updated_task = {}
    index = None
    for i, item in enumerate(tasks):
        if item["id"] == id:
            index = i
            break

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = {
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "id": id,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    tasks[index] = updated_task

    return updated_task


@router.delete("/task/{id}")
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            break

    return {"msg": "Task was deleted"}
