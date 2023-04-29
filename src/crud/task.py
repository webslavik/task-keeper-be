from sqlalchemy.orm import Session

from src.models.task import Task
from src.schemas.task import TaskBase, TaskUpdate


def read_tasks(db: Session):
    return db.query(Task).all()


def read_task(db: Session, id: int):
    return db.query(Task).filter(Task.id == id).first()


def create_task(db: Session, task: TaskBase):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(db: Session, id: int, task: TaskUpdate):
    db_task = read_task(db, id)
    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, id: int):
    db.query(Task).filter(Task.id == id).delete()
    db.commit()
