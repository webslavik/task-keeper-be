from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.schemas.task import TaskBase, TaskUpdate


class TaskRepository:
    @classmethod
    async def get_tasks(cls, db: AsyncSession, user_id: int) -> list[Task]:
        stmt = select(Task).where(Task.user_id == user_id)
        result = await db.scalars(stmt)

        return result.all()

    @classmethod
    async def get_task(cls, db: AsyncSession, task_id: int, user_id: int) -> Task:
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await db.scalars(stmt)

        return result.one_or_none()

    @classmethod
    async def create_task(cls, db: AsyncSession, task: TaskBase, user_id: int) -> Task:
        created_task = Task(**task.dict(), user_id=user_id)

        db.add(created_task)
        await db.commit()
        await db.refresh(created_task)

        return created_task

    @classmethod
    async def update_task(cls, db: AsyncSession, task_id: int, user_id: int, task: TaskUpdate) -> Task:
        found_task = await cls.get_task(db, task_id, user_id)

        found_task.title = task.title
        found_task.description = task.description
        found_task.completed = task.completed

        await db.commit()
        await db.refresh(found_task)

        return found_task

    @classmethod
    async def delete_task(cls, db: AsyncSession, task_id: int, user_id: int) -> None:
        found_task = await cls.get_task(db, task_id, user_id)

        await db.delete(found_task)
        await db.commit()
