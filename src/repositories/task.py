from sqlalchemy.orm import Session

from src.models.task import Task
from src.schemas.task import TaskBase, TaskUpdate


class TaskRepository:
    @classmethod
    def get_tasks(cls, db: Session, user_id: int) -> list[Task]:
        return db.query(Task).filter(Task.user_id == user_id).all()

    @classmethod
    def get_task(cls, db: Session, task_id: int, user_id: int) -> Task:
        return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    @classmethod
    def create_task(cls, db: Session, task: TaskBase, user_id: int) -> Task:
        created_task = Task(**task.dict(), user_id=user_id)
        db.add(created_task)

        try:
            db.commit()
        except Exception as error:
            db.rollback()
            raise RuntimeError("Failed to create task") from error

        return created_task

    @classmethod
    def update_task(cls, db: Session, task_id: int, user_id: int, task: TaskUpdate) -> Task:
        found_task = cls.get_task(db, task_id, user_id)
        found_task.title = task.title
        found_task.description = task.description
        found_task.completed = task.completed

        try:
            db.commit()
        except Exception as error:
            db.rollback()
            raise RuntimeError("Failed to create task") from error

        return found_task


    @classmethod
    def delete_task(cls, db: Session, task_id: int, user_id: int) -> None:
        try:
            db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).delete()
            db.commit()
        except Exception as error:
            db.rollback()
            raise RuntimeError("Failed to delete task") from error
