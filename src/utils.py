from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session


from src.repositories.user import UserRepository
from src.db_setup import get_db
from src.constants import SECRET_KEY, JWT_ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt


def check_authentication(authorization: str = Header(...)):
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        scheme, token = authorization.split()

        if scheme != "Bearer":
            raise credentials_exception

        payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)

        return payload
    except (ValueError, JWTError):
        raise credentials_exception
