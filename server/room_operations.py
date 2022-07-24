from __future__ import annotations

from typing import TYPE_CHECKING, Awaitable, Callable, Dict

from .db import db
from .utils import message_dict

if TYPE_CHECKING:
    from .rooms import RoomManager
    from .ws import SocketHandshake

__all__ = ("RECEIVER_OPERATIONS",)


async def _send_message(room: RoomManager, ws: SocketHandshake) -> None:
    await room.send_message(
        await ws.expect_only(
            {"content": str},
        ),
        await ws.get_user(),
    )


async def _get_messages(room: RoomManager, ws: SocketHandshake) -> None:
    take: int
    skip: int

    take, skip = await ws.expect(
        {
            "take": int,
            "skip": int,
        },
    )

    record = await db.room.find_unique(
        {
            "id": room.id,
        },
        include={
            "messages": {
                "take": take,
                "skip": skip,
                "include": {"author": True},
            }
        },
    )
    assert record

    await ws.reply(
        payload={
            "messages": [message_dict(i) for i in (record.messages or [])],
        }
    )


RECEIVER_OPERATIONS: Dict[
    str,
    Callable[
        [RoomManager, SocketHandshake],
        Awaitable[None],
    ],
] = {
    "send": _send_message,
    "getmessages": _get_messages,
}
