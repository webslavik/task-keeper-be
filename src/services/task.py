from sqlalchemy.orm import Session

from src.models.task import Task
from src.schemas.task import TaskBase, TaskCreate, TaskUpdate


class TaskService:
    @classmethod
    def get_task(cls, db: Session, task_id: int):
        return db.query(Task).get(task_id)

    @classmethod
    def create_task(cls, db: Session, task: TaskBase, user_id: int):
        created_task = Task(**task.dict(), user_id=user_id)
        db.add(created_task)

        try:
            db.commit()
            db.refresh(created_task)
        except Exception as error:
            db.rollback()
            raise RuntimeError("Failed to create task") from error

        return created_task

    @classmethod
    def update_task(cls, db: Session, task_id: int, task: TaskUpdate):
        found_task = cls.get_task(db, task_id)
        found_task.title = task.title
        found_task.description = task.description
        found_task.completed = task.completed

        try:
            db.commit()
            db.refresh(found_task)
        except Exception as error:
            db.rollback()
            raise RuntimeError("Failed to create task") from error

        return found_task


    @classmethod
    def delete_task(cls, db: Session, task_id: int):
        try:
            db.query(Task).filter(Task.id == task_id).delete()
            db.commit()
        except Exception as error:
            db.rollback()
            raise RuntimeError("Failed to delete task") from error
