import random
import string
from dataclasses import dataclass
from typing import Awaitable, Callable, Dict

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from .db import db
from .ws import SocketHandshake

hasher = PasswordHasher()

__all__ = ("operations",)

OperationFunc = Callable[[SocketHandshake], Awaitable[None]]


@dataclass
class Operation:
    """Dataclass for holding session operation information."""

    fn: OperationFunc
    limit: int = -1
    count: int = 0


def _create_string(length: int = 8) -> str:
    return "".join([random.choice(string.ascii_letters) for _ in range(length)])


async def register(ws: SocketHandshake):
    """Register an account."""
    username, password = await ws.expect(
        {
            "username": str,
            "password": str,
        }
    )

    found = await db.user.find_many(where={"name": username})
    tag: int = len(found) + 1

    record = await db.user.create(
        {
            "name": username,
            "password": hasher.hash(password),
            "tag": tag,
        }
    )

    ws.socket.user_id = record.id
    await ws.success(payload={"tag": tag})


async def login(ws: SocketHandshake):
    """Log in to an account."""
    username, password, tag = await ws.expect(
        {"username": str, "password": str, "tag": int}
    )

    user = await db.user.find_first(
        where={"name": username, "tag": tag},
    )

    if not user:
        await ws.error("Invalid username or password.")

    try:
        hasher.verify(user.password, password)
    except VerifyMismatchError:
        await ws.error("Invalid username or password.")

    ws.socket.user_id = user.id
    await ws.success()


async def create_room(ws: SocketHandshake):
    """Create a new room."""
    name: str = await ws.expect_only(
        {"name": str},
        ensure_logged=True,
    )

    uid: int = await ws.get_user()

    user = await db.user.find_unique({"id": uid})
    assert user

    record = await db.room.create(
        {
            "name": name,
            "code": _create_string(),
            "users": {"connect": {"id": user.id}},
        }
    )
    rid: int = record.id

    await db.user.update(
        {
            "servers": {"connect": [{"id": rid}]},
        },
        where={"id": uid},
    )

    await ws.success(payload={"id": rid})


async def join(ws: SocketHandshake):
    """Join a new room."""
    code: str = await ws.expect_only(
        {"code": str},
        ensure_logged=True,
    )

    uid: int = await ws.get_user()
    room = await db.room.update(
        {
            "users": {
                "connect": [
                    {"id": uid},
                ]
            }
        },
        where={"code": code},
    )

    if not room:
        await ws.error("Invalid room code.")

    await db.user.update(
        {
            "servers": {
                "connect": [
                    {"id": room.id},
                ]
            }
        },
        where={"id": uid},
    )

    await ws.success(payload={"id": room.id})


# the key here is the type sent by the client
operations: Dict[str, Operation] = {
    "register": Operation(register, 1),
    "login": Operation(login, 1),
    "createroom": Operation(create_room),
    "joinroom": Operation(join),
}
