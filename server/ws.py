from typing import Any, Dict, List, NoReturn, Optional

from fastapi import WebSocket

from .utils import err, recv, verify

__all__ = (
    "SocketHandshake",
    "Socket",
)


class SocketHandshake:
    """Class for handling a WebSocket handshake."""

    def __init__(self, socket: "Socket", payload: dict) -> None:
        self._socket = socket
        self._ws = socket.connection
        self._reload(payload)

    @property
    def payload(self) -> dict:
        """Current received payload."""
        return self._payload

    @property
    def socket(self) -> "Socket":
        """Parent Socket object."""
        return self._socket

    @property
    def handshake_type(self) -> str:
        """Type header of the current payload."""
        return self._type

    async def _ensure_logged(self) -> None:
        if not self.socket.user_id:
            await self.error(
                "You must be authenticated to perform this operation.",
            )

    async def expect(
        self,
        schema: Dict[str, type],
        *,
        ensure_logged: bool = False,
    ) -> List[Any]:
        """Get a JSON value from the socket handshake."""
        if ensure_logged:
            await self._ensure_logged()

        return await verify(self._ws, self._payload, schema)

    async def expect_only(
        self,
        schema: Dict[str, type],
        *,
        ensure_logged: bool = False,
    ) -> Any:
        """Get a single JSON value from the socket handshake."""
        return (await self.expect(schema, ensure_logged=ensure_logged))[0]

    async def error(self, message: str, done: bool = True) -> NoReturn:
        """Send an error back to the client."""
        await err(self._ws, message, self._payload, done=done)

    async def receive_next(
        self,
        schema: Dict[str, type],
        *,
        ensure_logged: bool = False,
    ) -> List[Any]:
        """Receive the next message in the handshake."""
        if ensure_logged:
            await self._ensure_logged()

        payload = await recv(self._ws, schema)
        self._reload(payload)
        return [payload[i] for i in schema]

    def _reload(self, payload: dict) -> None:
        self._payload: dict = payload
        self._type: str = payload["type"]

    async def reply(
        self,
        *,
        success: bool = True,
        done: bool = False,
        payload: Optional[dict] = None,
        message: Optional[str] = None,
    ):
        """Send a response to the client."""
        res = {
            "type": self._type,
            "done": done,
            "message": message,
            "success": success,
            **(payload or {}),
        }

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

    async def success(
        self,
        *,
        message: Optional[str] = None,
        payload: Optional[dict] = None,
    ):
        """Send a final success response to the client."""
        await self.finalize(
            success=True,
            message=message,
            payload=payload,
        )

    async def get_user(self) -> int:
        """Get the current authenticated user."""
        await self._ensure_logged()
        uid = self.socket.user_id
        assert uid is not None  # just to make mypy happy

        return uid


class Socket:
    """Class for wrapping around a WebSocket."""

    def __init__(self, ws: WebSocket) -> None:
        self._ws = ws
        self._user_id: Optional[int] = None

    @property
    def user_id(self) -> Optional[int]:
        """ID of the current authenticated user."""
        return self._user_id

    @user_id.setter
    def user_id(self, id: int) -> None:
        self._user_id = id

    async def accept(self) -> SocketHandshake:
        """Accept an incoming handshake request."""
        return SocketHandshake(self, await recv(self._ws))

    async def close(self) -> None:
        """Close the socket."""
        await self._ws.close()

    async def connect(self):
        """Connect to the client."""
        await self._ws.accept()

    @property
    def connection(self) -> WebSocket:
        """Raw WebSocket object."""
        return self._ws
