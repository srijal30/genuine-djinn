from fastapi import FastAPI

from .db import db
from .socket_router import router

__all__ = ("app",)

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup():
    await db.connect()
