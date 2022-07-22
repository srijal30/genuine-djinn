from __future__ import annotations

from typing import Any, Dict, List, NoReturn, Optional

from fastapi import WebSocket

from .utils import err, recv, verify

__all__ = (
    "SocketHandshake",
    "Socket",
)


class SocketHandshake:
    """Class for handling a WebSocket handshake."""

    def __init__(self, ws: WebSocket, payload: dict) -> None:
        self._ws = ws
        self._reload(payload)

    @property
    def payload(self) -> dict:
        """Current received payload."""
        return self._payload

    @property
    def handshake_type(self) -> str:
        """Type header of the current payload."""
        return self._type

    async def expect(self, schema: Dict[str, type]) -> List[Any]:
        """Get a JSON value from the socket handshake."""
        return await verify(self._ws, self._payload, schema)

    async def error(self, message: str, done: bool = True) -> NoReturn:
        """Send an error back to the client."""
        await err(self._ws, message, self._payload, done=done)

    async def receive_next(self, schema: Dict[str, type]) -> List[Any]:
        """Receive the next message in the handshake."""
        payload = await recv(self._ws, schema)
        self._reload(payload)
        return [payload[i] for i in schema]

    def _reload(self, payload: dict) -> None:
        self._payload: dict = payload
        self._type: str = payload["type"]

    async def reply(
        self,
        *,
        success: Optional[bool] = None,
        done: bool = False,
        payload: Optional[dict] = None,
        message: Optional[str] = None,
    ):
        """Send a response to the client."""
        res = {
            "type": self._type,
            "done": done,
        }

        if success is not None:
            res["success"] = success

        if payload is not None:
            res = {**res, **payload}

        if message is not None:
            res["message"] = message

        await self._ws.send_json(res)

    async def finalize(
        self,
        *,
        success: bool,
        message: Optional[str] = None,
        payload: Optional[dict] = None,
    ):
        """Send a final response to the client."""
        await self.reply(
            success=success,
            message=message,
            payload=payload,
            done=True,
        )


class Socket:
    """Class for wrapping around a WebSocket."""

    def __init__(self, ws: WebSocket) -> None:
        self._ws = ws

    async def accept(self) -> SocketHandshake:
        """Accept an incoming handshake request."""
        return SocketHandshake(self._ws, await recv(self._ws))

    async def close(self) -> None:
        """Close the socket."""
        await self._ws.close()

    async def connect(self):
        """Connect to the client."""
        await self._ws.accept()
