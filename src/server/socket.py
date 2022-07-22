from contextlib import suppress
from typing import Awaitable, Callable, Dict

from argon2 import PasswordHasher
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .db import db
from .ws import Socket, SocketHandshake

ROOMS: Dict[str, str] = {}

router = APIRouter(prefix="/ws")
hasher = PasswordHasher()


async def _register(ws: SocketHandshake):
    username, password = await ws.receive_next(
        {
            "username": str,
            "password": str,
        }
    )

    found = await db.user.find_many(where={"name": username})
    tag: int = len(found) + 1

    await db.user.create(
        {
            "name": username,
            "password": hasher.hash(password),
            "tag": tag,
        }
    )

    await ws.finalize(success=True, payload={"tag": tag})


OPERATIONS: Dict[str, Callable[[SocketHandshake], Awaitable[None]]] = {
    "register": _register,
}


@router.websocket("/")
async def socket(raw_socket: WebSocket):
    """Main socket for handling client-server communication."""
    ws = Socket(raw_socket)
    await ws.connect()

    with suppress(WebSocketDisconnect):
        while True:
            handshake = await ws.accept()
            fn = OPERATIONS.get(handshake.handshake_type)

            if not fn:
                await handshake.error("Invalid type was passed.")

            await fn(handshake)
