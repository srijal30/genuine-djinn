import copy
from contextlib import suppress

from argon2 import PasswordHasher
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .operations import operations
from .utils import EndHandshake
from .ws import Socket

__all__ = ("router",)

router = APIRouter()
hasher = PasswordHasher()


@router.websocket("/ws")
async def socket(raw_socket: WebSocket):
    """Main socket for handling client-server communication."""
    ws = Socket(raw_socket)
    await ws.connect()

    ops = copy.deepcopy(operations)

    with suppress(WebSocketDisconnect, EndHandshake):
        while True:
            handshake = await ws.accept()

            operation = ops.get(handshake.handshake_type)

            if not operation:
                await handshake.error("Invalid type was passed.")

            if operation.limit == operation.count:
                await handshake.error("Limit exceeded for operation.")

            await operation.fn(handshake)

            operation.count += 1
