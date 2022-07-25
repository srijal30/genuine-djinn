import json
from typing import Any, Callable, Dict, List, Tuple

import websockets

DOMAIN = "ws://localhost:5000"
ROUTE = "/ws"
URL = DOMAIN + ROUTE

# completed ones
# login
# register
# create room
# logout
# join room
# connect to room
# list rooms

# not sure but probaly done
# send messages
# exit a room

# not sure but probably not done
# receive messages


class SocketClient():
    """API Wrapper that handles all client side communication with the server."""

    def __init__(self):
        self.connected = False  # temprorary state system

    # temprorary solution until figure out how to use __new__ instead of __init__
    async def connect(self):
        """Connects to the server. Must be called in order for everything to work."""
        self.ws: websockets.WebSocketClientProtocol = await websockets.connect(URL)

    async def receive(self) -> Dict[str, Any]:
        """Receives a message from server and returns as dict."""
        res = await self.ws.recv()
        return json.loads(res)

    async def send(
        self,
        type: str,
        payload: Dict[str, Any],
        reply: bool = True
    ) -> Dict[str, Any]:
        """
        Sends a message to the server and returns the response.

        Specify type of request, payload data, and if reply is expected (by default yes)
        """
        req = json.dumps({
            "type": type,
            **payload
        })
        await self.ws.send(req)
        if reply:
            return await self.receive()
        else:
            return {}

    async def login(self, username: str, tag: int, password: str) -> bool:
        """
        Sends a login request to the server.

        Returns True if it was succesful and False if not.
        """
        payload = {
            "username": username,
            "tag": tag,
            "password": password
        }
        res = await self.send("login", payload)
        return res['success']

    # Will this work when user is not currently logged in?
    async def logout(self) -> bool:
        """
        Logs out the user.

        Returns if successful or not.
        """
        res = await self.send("logout", {})
        return res['success']

    async def register(self, username: str, password: str) -> int:
        """
        Sends a register request to the server.

        Returns the unique user tag of the new user.
        """
        payload = {
            "username": username,
            "password": password
        }
        res = await self.send("register", payload)
        return res["tag"]

    async def create_room(self, name: str) -> Tuple[int, int]:
        """
        Asks the server to create a room with given name. Also joins room.

        Returns (roomcode, roomid) of the newly created room.
        Cannot fail. Authentication is required.
        """
        payload = {
            "name": name
        }
        res = await self.send("createroom", payload)
        return (res['code'], res['id'])

    # MAKE SURE THAT THE TYPE 'CREATEROOM' is not a typo (it was a typo)
    # There might be an issue with the return in the case that not successful.
    async def join_room(self, code: str) -> int:
        """
        Joins the room with given code.

        Returns id of the joined room.
        Authentication required.
        """
        payload = {
            'code': code
        }
        res = await self.send("joinroom", payload)
        return res['id']

    # maybe add state management here? (i added temp one for now)
    async def connect_room(self, id: int) -> bool:
        """
        Connects to a chatroom.

        Returns whether connection was successful or not.
        Authentication required. Joining room required.
        """
        payload = {
            "id": id
        }
        res = await self.send("roomconnect", payload)
        self.connected = res['success']
        # turn on the message receive listener?
        return res['success']

    async def start_receive_messages(self, callback: Callable[[str], None]) -> None:
        """
        Starts a message receiving listener.

        When a message is received, callback function is called.
        Authentication required. Connected room required.
        """
        while self.connected:
            potential_msg = await self.receive()
            if 'new' not in potential_msg:
                continue
            else:
                callback(potential_msg['new'])

    # will the server send back a message after receiving a message send request?
    # are we expecting a reply from the server?
    # rn assuming no
    async def send_message(self, message: str) -> bool:
        """
        Sends a message to the server.

        Does not expect a reply from the server.
        Authentication required. Connected room required.
        """
        payload = {
            'message': message
        }
        await self.send("roomconnect", payload, reply=False)
        return True  # rn no way to fail?

    # are we expecting a reply from the server here??
    # rn assuming no
    async def exit_room(self) -> bool:
        """
        Exits the currently connected room.

        Returns whether succesful or not.
        Authentication required. Connected room required.
        """
        payload = {
            'end': True
        }
        await self.send("roomconnect", payload, reply=False)
        self.connected = False
        return True  # rn no way to fail?

    async def list_rooms(self) -> List[Dict[str, Any]]:
        """
        Asks server for a list of rooms that the current user has joined.

        Returns list of connected rooms.
        Authentication required. Operation cannot fail.
        """
        res = await self.send("listrooms", {})
        return res['servers']
