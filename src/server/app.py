from fastapi import FastAPI

from .socket_router import router

__all__ = ("app",)

app = FastAPI()

app.include_router(router)
