from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import tasks, auth
from src.constants import ALLOWED_ORIGINS


def init_api() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(tasks.router)
    app.include_router(auth.router)

    return app


app = init_api()
