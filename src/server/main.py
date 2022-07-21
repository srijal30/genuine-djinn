from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()


@app.websocket("/")
async def socket(ws: WebSocket):
    await ws.accept()
    await ws.send_text("hello world")
    await ws.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
