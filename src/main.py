from fastapi import FastAPI

from src.api import tasks
from src.db_setup import engine
from src.models import task

task.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)
