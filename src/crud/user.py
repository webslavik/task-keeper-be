from sqlalchemy.orm import Session

from src.schemas.user import UserBase
from src.models.user import User


def get_user_by_id(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserBase):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, id: int()):
    db.query(User).filter(User.id == id).delete()
    db.commit()
