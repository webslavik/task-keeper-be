from fastapi import FastAPI

from src.db_setup import engine
from src.models import task, user
from src.api import tasks, auth


def init_api() -> FastAPI:
    task.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)

    app = FastAPI()

    app.include_router(tasks.router, tags=["Tasks"], prefix="/api/users")
    app.include_router(auth.router, tags=["Auth"], prefix="/api/auth")

    return app


app = init_api()
