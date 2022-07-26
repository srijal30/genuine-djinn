from fastapi import FastAPI

from .db import db, make_system
from .socket_router import router

__all__ = ("app",)

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup():
    await db.connect()
    await make_system()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
