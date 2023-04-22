from fastapi import FastAPI

from api import tasks
from db_setup import engine
from models import task

task.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)
