from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

from fastapi import WebSocketDisconnect

from .db import db
from .utils import EndHandshake, references, user_dict

if TYPE_CHECKING:
    from .ws import SocketHandshake
    from prisma.models import Room, User

from .room_operations import RECEIVER_OPERATIONS


class RoomManager:
    """Class for managing rooms via socket handshakes."""

    def __init__(
        self,
        room_id: int,
    ) -> None:
        self._id = room_id
        self._connected: List[SocketHandshake] = []

    async def _lookup(self) -> Room:
        room = await db.room.find_unique(
            {"id": self.id},
        )
        assert room

        return room

    async def send_message(
        self,
        message: str,
        author: Union[User, int],
    ) -> None:
        """Send a message in a room."""
        au = (
            author
            if not isinstance(author, int)
            else await db.user.find_unique({"id": author})
        )
        assert au

        for i in self._connected:
            await i.reply(
                message="New message received.",
                payload={
                    "new": {
                        "author": user_dict(au),
                        "content": message,
                    },
                },
            )

        record = await db.message.create(
            {
                "content": message,
                "author": references(au.id),
                "server": references(self.id),
            }
        )
        await db.room.update(
            {"messages": references(record.id, array=True)},
            where={"id": self.id},
        )
        await db.user.update(
            {"messages": references(record.id)},
            where={"id": au.id},
        )

    @property
    def id(self) -> int:
        """ID of the room."""
        return self._id

    async def register_handshake(self, socket: SocketHandshake) -> None:
        """Add a socket to the connected handshakes."""
        self._connected.append(socket)

        await socket.reply(message="Connection established.")
        await self._setup_receiver(socket)

    async def _setup_receiver(
        self,
        ws: SocketHandshake,
    ) -> None:
        while True:
            try:
                (action,) = await ws.receive_next({"action": str})
            except (WebSocketDisconnect, EndHandshake) as e:
                self._connected.remove(ws)
                raise e

            caller = RECEIVER_OPERATIONS.get(action)

            if not caller:
                await ws.error("Invalid action.", done=False)

            try:
                await caller(self, ws)
            except EndHandshake as e:
                # maybe make this catch WebSocketDisconnect as well?
                self._connected.remove(ws)
                raise e
