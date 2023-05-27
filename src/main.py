from fastapi import FastAPI

import src.constants
from src.db_setup import engine
from src.models import task, user
from src.api import tasks, auth


def init_api() -> FastAPI:
    task.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)

    app = FastAPI()

    app.include_router(tasks.router)
    app.include_router(auth.router)

    return app


app = init_api()
