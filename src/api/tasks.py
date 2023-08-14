from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.task import TaskBase, TaskUpdate, Task
from src.db_setup import get_db

from src.repositories.task import TaskRepository
from src.helpers import check_authentication, get_current_user


router = APIRouter(
    tags=["Tasks"],
    prefix="/api/tasks",
    dependencies=[Depends(check_authentication)]
)


@router.get("")
async def get_tasks(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tasks = await TaskRepository.get_tasks(db, current_user.id)

    return {"tasks": tasks}


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Task)
async def create_task(task: TaskBase, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_task = await TaskRepository.create_task(db, task, current_user.id)

    return db_task


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_task = await TaskRepository.get_task(db, task_id, current_user.id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return db_task


@router.patch("/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_task = await TaskRepository.get_task(db, task_id, current_user.id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = await TaskRepository.update_task(db, task_id, current_user.id, task=task)

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_task = await TaskRepository.get_task(db, task_id, current_user.id)

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    await TaskRepository.delete_task(db, task_id, current_user.id)
