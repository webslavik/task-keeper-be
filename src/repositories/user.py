from sqlalchemy.orm import Session

from src.schemas.user import UserBase
from src.models.user import User


class UserService:
    @classmethod
    def get_user_by_id(cls, db: Session, user_id: str):
        return db.query(User).get(user_id)


    @classmethod
    def get_user_by_email(cls, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()


    @classmethod
    def create_user(cls, db: Session, user: UserBase):
        created_user = User(**user.dict())

        db.add(created_user)

        try:
            db.commit()
            db.refresh(created_user)
        except Exception as error:
            db.rollback()
            raise RuntimeError("Failed to create user") from error

        return created_user
