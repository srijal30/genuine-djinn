import uvicorn  # type: ignore
from fastapi import FastAPI

from .socket import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
