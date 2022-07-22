from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from contextlib import suppress
from .utils import recv
import string
import random
from typing import Dict

ROOMS: Dict[str, str] = {}

router = APIRouter(prefix="/room")


@router.websocket("/")
async def socket(ws: WebSocket):
    """Main socket for room handling."""
    await ws.accept()

    with suppress(WebSocketDisconnect):
        while True:
            data = await recv(ws)
