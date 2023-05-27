from fastapi import FastAPI

from src.db_setup import engine
from src.models import task, user
from src.api import tasks, auth

task.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)
app.include_router(auth.router)
