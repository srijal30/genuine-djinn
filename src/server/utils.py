import json
from typing import Any, Dict, List, NoReturn, Optional

from fastapi import WebSocket, WebSocketDisconnect

__all__ = (
    "err",
    "recv",
    "verify",
)


async def err(
    socket: WebSocket,
    message: str,
    data: Optional[dict] = None,
    done: bool = True,
) -> NoReturn:
    """Send an error back to the user."""
    await socket.send_json(
        {
            "type": (data or {}).get("type") or "unknown",
            "message": message,
            "done": done,
            "success": False,
        }
    )
    await socket.close()
    raise WebSocketDisconnect


async def verify(
    socket: WebSocket,
    origin: dict,
    data: Dict[str, type],
) -> List[Any]:
    """Validate a received object."""
    keys = [*data.keys(), "type"]
    success: bool = all([origin.get(i) for i in keys])

    if not success:
        missing: str = ", ".join([i for i in keys if not data.get(i)])
        await err(socket, f"Object missing keys: {missing}", data)

    for key, ntype in data.items():
        value = origin[key]

        if not isinstance(value, ntype):
            await err(
                socket, f'"{key}" got wrong type: expected {ntype}, got {type(value)}'
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

    await verify(socket, data, schema)
    return data
