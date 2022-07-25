from __future__ import annotations

from typing import (
    TYPE_CHECKING, Awaitable, Callable, Dict, Literal, Optional, Union,
    overload
)

from .db import db
from .utils import message_dict

if TYPE_CHECKING:
    from prisma.models import Message

    from .rooms import RoomManager
    from .ws import SocketHandshake

__all__ = ("RECEIVER_OPERATIONS",)


async def _send_message(room: RoomManager, ws: SocketHandshake) -> None:
    content: str
    content = await ws.expect_only({"content": str})

    if len(content) > 2500:
        return await ws.error_continue(
            "Content cannot exceed 2500 characters.",
        )

    await room.send_message(
        content,
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


@overload
async def _handle_message_lookup(
    ws: SocketHandshake,
    *,
    return_id: Literal[False] = False,
) -> Optional[Message]:
    ...


@overload
async def _handle_message_lookup(
    ws: SocketHandshake,
    *,
    return_id: Literal[True] = True,
) -> Optional[int]:
    ...


async def _handle_message_lookup(
    ws: SocketHandshake,
    *,
    return_id: bool = False,
) -> Optional[Union[Message, int]]:
    mid = await ws.expect_only(
        {
            "mid": int,
        }
    )

    message = await db.message.find_unique({"id": mid})

    if not message:
        await ws.error_continue(
            "Message not found.",
        )
        return None  # mypy is getting angry

    uid = ws.get_user_id()

    if not message.author_id == uid:
        await ws.error_continue(
            "Only the author can edit their message.",
        )
        return None

    return message if not return_id else mid


async def _edit(room: RoomManager, ws: SocketHandshake) -> None:
    mid = await _handle_message_lookup(ws, return_id=True)

    if not mid:
        return  # pass back the error

    content = await ws.expect_only({"content": str})

    if len(content) > 2500:
        return await ws.error_continue(
            "Content cannot exceed 2500 characters.",
        )

    await db.message.update(
        {"content": content},
        where={"id": mid},
    )
    await room.update_message(mid, content)


async def _delete(room: RoomManager, ws: SocketHandshake) -> None:
    mid = await _handle_message_lookup(ws, return_id=True)

    if not mid:
        return

    await db.message.delete({"id": mid})
    await room.delete_message(mid)


RECEIVER_OPERATIONS: Dict[
    str,
    Callable[
        [RoomManager, SocketHandshake],
        Awaitable[None],
    ],
] = {
    "send": _send_message,
    "getmessages": _get_messages,
    "edit": _edit,
    "delete": _delete,
}
