from fastapi import FastAPI

from api import task

app = FastAPI()

app.include_router(task.router)
