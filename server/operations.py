from dataclasses import dataclass
from typing import Awaitable, Callable, Dict

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from .db import db
from .rooms import RoomManager
from .utils import create_string, references, room_dict
from .ws import SocketHandshake

hasher = PasswordHasher()

__all__ = ("operations",)

OperationFunc = Callable[[SocketHandshake], Awaitable[None]]
ROOMS: Dict[int, RoomManager] = {}


@dataclass
class Operation:
    """Dataclass for holding session operation information."""

    fn: OperationFunc
    limit: int = -1
    count: int = 0


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


async def login(ws: SocketHandshake) -> None:
    """Log in to an account."""
    if ws.socket.user_id:
        await ws.error("Already logged in.")
    username, password, tag = await ws.expect(
        {
            "username": str,
            "password": str,
            "tag": int,
        }
    )

    user = await db.user.find_first(
        where={
            "name": username,
            "tag": tag,
        },
    )

    if not user:
        await ws.error("Invalid username or password.")

    try:
        hasher.verify(user.password, password)
    except VerifyMismatchError:
        await ws.error("Invalid username or password.")

    ws.socket.user_id = user.id
    await ws.success()


async def create_room(ws: SocketHandshake) -> None:
    """Create a new room."""
    name: str = await ws.expect_only(
        {"name": str},
        ensure_logged=True,
    )

    user = await ws.get_user()
    record = await db.room.create(
        {
            "name": name,
            "code": create_string(),
            "users": references(user.id),
        }
    )
    rid: int = record.id

    await db.user.update(
        {
            "servers": references(rid, array=True),
        },
        where={"id": user.id},
    )

    await ws.success(payload={"id": rid})


async def join(ws: SocketHandshake) -> None:
    """Join a new room."""
    code: str = await ws.expect_only(
        {"code": str},
        ensure_logged=True,
    )

    uid: int = await ws.get_user_id()
    room = await db.room.update(
        {"users": references(uid, array=True)},
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


async def list_rooms(ws: SocketHandshake) -> None:
    """List rooms of the current user."""
    user = await ws.get_user(
        include={
            "servers": {
                "include": {
                    "users": True,
                }
            },
        }
    )

    await ws.success(
        payload={
            "servers": [room_dict(i) for i in (user.servers or [])],
        }
    )


async def room_connect(ws: SocketHandshake) -> None:
    """Connect to a room."""
    rid = await ws.expect_only(
        {
            "id": int,
        },
        ensure_logged=True,
    )

    room = await db.room.find_first(
        where={
            "id": rid,
            "users": {
                "some": {
                    "id": await ws.get_user_id(),
                }
            },
        }
    )

    if not room:
        await ws.error("Invalid room ID.")

    rid = room.id
    manager = ROOMS.get(rid)

    if not manager:
        manager = RoomManager(rid)
        ROOMS[rid] = manager

    await manager.register_handshake(ws)


async def logout(ws: SocketHandshake) -> None:
    await ws.get_user_id()  # to ensure that they are authenticated already
    ws.socket.user_id = None
    await ws.success()


# the key here is the type sent by the client
operations: Dict[str, Operation] = {
    "register": Operation(register, 1),
    "login": Operation(login, 1),
    "createroom": Operation(create_room),
    "joinroom": Operation(join),
    "listrooms": Operation(list_rooms),
    "roomconnect": Operation(room_connect),
    "logout": Operation(logout),
}
"""Dictionary containing resolvers for type headers."""
