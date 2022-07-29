from __future__ import annotations

import json
import random
import string
from typing import TYPE_CHECKING, Any, Dict, List, NoReturn, Optional

from fastapi import WebSocket

from .db import db

if TYPE_CHECKING:
    from prisma.models import Message, Room, User

__all__ = (
    "err",
    "recv",
    "verify",
    "references",
    "user_dict",
    "create_string",
    "message_dict",
    "room_dict",
    "find_room_for",
)


class EndHandshake(Exception):
    """Exception to end the current handshake without killing the connection."""


async def find_room_for(room_id: int, user_id: int) -> Optional[Room]:
    """Find a room that contains a user."""
    return await db.room.find_first(
        where={
            "id": room_id,
            "users": {
                "some": {
                    "id": user_id,
                }
            },
        },
    )


def references(
    target: Any,
    *,
    name: str = "id",
    array: bool = False,
    disconnect: bool = False,
) -> Any:
    """Create a Prisma relation dictionary."""
    raw = {name: target}
    return {
        "connect"
        if not disconnect
        else "disconnect": raw
        if not array
        else [raw],  # fmt: off
    }


def create_string(length: int = 8) -> str:
    """Create a random string (not cryptograhpically secure)."""
    return "".join(
        [random.choice(string.ascii_lowercase) for _ in range(length)],
    )


def user_dict(user: User) -> dict:
    """Make a public dictionary for a user object."""
    return {
        "name": user.name,
        "tag": user.tag,
        "id": user.id,
    }


def room_dict(room: Room) -> dict:
    """Make a public dictionary for a room object."""
    res = room.__dict__
    del res["messages"]
    res["users"] = [user_dict(i) for i in res["users"]]
    return res


def message_dict(message: Message) -> dict:
    """Make a public dictionary for a message object."""
    res = message.__dict__
    res["author"] = user_dict(res["author"])

    for i in {"server", "server_id", "author_id"}:
        del res[i]

    res["created_at"] = res["created_at"].timestamp()

    return res


async def _send(
    socket: WebSocket,
    message: str,
    done: bool,
    success: bool,
    data: Optional[dict] = None,
) -> None:
    """Send an message back to the user."""
    await socket.send_json(
        {
            "type": (data or {}).get("type") or "unknown",
            "message": message,
            "done": done,
            "success": success,
        }
    )


async def err(
    socket: WebSocket,
    message: str,
    data: Optional[dict] = None,
) -> NoReturn:
    """Send an error back to the user."""
    await _send(socket, message, True, False, data)
    raise EndHandshake


async def verify(
    socket: WebSocket,
    origin: dict,
    data: Dict[str, type],
) -> List[Any]:
    """Validate a received object."""
    keys = data.keys()
    success: bool = all([origin.get(i) is not None for i in keys])

    if not success:
        missing: str = ", ".join(
            [i for i in keys if origin.get(i) is None],
        )
        await err(socket, f"Payload missing keys: {missing}", origin)

    for key, ntype in data.items():
        value = origin[key]

        if not isinstance(value, ntype):
            await err(
                socket,
                f'"{key}" got wrong type: expected {ntype.__name__}, got {type(value).__name__}',
            )

    return [origin[i] for i in data]


async def recv(
    socket: WebSocket,
    schema_data: Optional[Dict[str, type]] = None,
) -> Dict[str, Any]:
    """Receive, parse, and validate an object received through the WebSocket connection."""
    schema = schema_data or {}
    schema["type"] = str

    try:
        data: dict = json.loads(await socket.receive_text())
    except json.JSONDecodeError:
        await err(socket, "Invalid JSON object.")

    if data.get("end"):
        await _send(socket, "Ended handshake.", True, True)
        raise EndHandshake

    await verify(socket, data, schema)
    return data
