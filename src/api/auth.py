from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.utils import get_hashed_password, verify_password, create_access_token

from src.db_setup import get_db
from src.schemas.user import UserRegister, UserLogin
from src.repositories.user import UserRepository
from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Auth"], prefix="/api/auth")


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = UserRepository.get_user_by_email(db, user.email)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = UserRepository.get_user_by_email(db, user.email)

    if db_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user.password = get_hashed_password(user.password)

    UserRepository.create_user(db, user)

    return {"message": "User was created"}
