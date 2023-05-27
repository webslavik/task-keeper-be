import os
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Header, HTTPException, status


secret_key = os.getenv("SECRET_KEY")
jwt_algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

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
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=jwt_algorithm)

    return encoded_jwt

# TODO: Temprorary solution, put it here
async def check_authentication_token(authorization: str = Header(...)):
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        scheme, token = authorization.split()

        if scheme != "Bearer":
            raise credentials_exception

        payload = jwt.decode(token, secret_key, algorithms=jwt_algorithm)
        
        return payload
    except (ValueError, JWTError):
        raise credentials_exception
