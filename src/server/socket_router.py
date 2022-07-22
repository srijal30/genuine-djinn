from contextlib import suppress
from dataclasses import dataclass
from typing import Awaitable, Callable, Dict

from argon2 import PasswordHasher
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .db import db
from .ws import Socket, SocketHandshake

OperationFunc = Callable[[SocketHandshake], Awaitable[None]]

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


@dataclass
class Operation:
    """Dataclass for holding session operation information."""

    fn: OperationFunc
    count: int
    limit: int


@router.websocket("/")
async def socket(raw_socket: WebSocket):
    """Main socket for handling client-server communication."""
    ws = Socket(raw_socket)
    await ws.connect()

    operations: Dict[str, Operation] = {
        "register": Operation(_register, 0, 1),
    }

    with suppress(WebSocketDisconnect):
        while True:
            handshake = await ws.accept()
            operation = operations.get(handshake.handshake_type)

            if not operation:
                await handshake.error("Invalid type was passed.")

            if operation.limit == operation.count:
                await handshake.error("Limit exceeded for operation.")

            await operation.fn(handshake)
            operation.count += 1
