import os
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DB_USER_TEST = os.getenv("DB_USER_TEST")
DB_PASSWORD_TEST = os.getenv("DB_PASSWORD_TEST")
DB_HOST_TEST = os.getenv("DB_HOST_TEST")
DB_NAME_TEST = os.getenv("DB_NAME_TEST")

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ALLOWED_ORIGINS = [
    'https://task-keeper-fe.onrender.com',
    'http://localhost:3000'
]
