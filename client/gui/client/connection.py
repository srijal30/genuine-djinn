import json
from typing import Any, Callable, Dict, List, Tuple

import websockets

DOMAIN = "ws://192.155.88.143:5005"
# DOMAIN = "ws://localhost:5000"
ROUTE = "/ws"
URL = DOMAIN + ROUTE

# login
# register
# create room
# logout
# join room
# connect to room
# list rooms
# exit a room
# send messages ~ double check
# receive messages ~ double check
# getting message history ~ not done


# add what ip to connect to in the constructor?
# add a __new__ method so that we can call connect on construction
class SocketClient():
    """API Wrapper that handles all client side communication with the server."""

    connected_to_room = False

    async def connect(self):
        """Connects to the server. Must be called in order for everything to work."""
        self.ws = await websockets.connect(URL)
        print('connected!')

    async def _receive(self) -> Dict[str, Any]:
        """Receives a message from the server. Converts raw data to python dict."""
        res = await self.ws.recv()
        return json.loads(res)

    async def _send(
        self,
        type: str,
        payload: Dict[str, Any],
        reply: bool = True
    ) -> Dict[str, Any]:
        """Sends a message to the server. Expects no reply by default."""
        req = json.dumps({
            "type": type,
            **payload
        })
        await self.ws.send(req)
        if reply:
            return await self._receive()
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
        res = await self._send("login", payload)
        print(res)
        return res['success']

    async def logout(self) -> bool:
        """
        Logs out the user.

        Returns if successful or not.
        """
        res = await self._send("logout", {})
        return res['success']

    async def register(self, username: str, password: str) -> int:
        """
        Sends a register request to the server. Also logs user in.

        Returns the unique user tag of the new user.
        """
        payload = {
            "username": username,
            "password": password
        }
        res = await self._send("register", payload)
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
        res = await self._send("createroom", payload)
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
        res = await self._send("joinroom", payload)
        print(res)
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
        res = await self._send("roomconnect", payload)
        self.connected_to_room = res['success']
        return res['success']

    # check what msg is, is it a json or string???
    async def receive_messages(self, callback: Callable[[str], None]) -> None:
        """
        Starts a message receiving listener.

        When a message is received, callback function is called on the new message.
        Authentication required. Connected room required.
        """
        async for res in self.ws:
            # makes sure that there is a way for loop to end
            if not self.connected_to_room:
                print('stopped receicving')  # see if we even neee Task.cancel()
                break
            res = json.loads(res)
            # make sure that handler not stealing non message requests
            if res['type'] != 'roomconnect':
                raise(BaseException('Message Handler Received an Incorrect Message'))
            msg = res['new']
            callback(msg)

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
            'content': message,
            'action': 'send'
        }
        await self._send("roomconnect", payload, reply=False)
        return True  # rn no way to fail?

    # add code to check if there is a current room
    async def exit_room(self) -> bool:
        """
        Exits the currently connected room.

        Returns whether succesful or not.
        Authentication required. Connected room required.
        """
        payload = {
            'end': True
        }
        res = await self._send("roomconnect", payload, reply=False)
        if res['success']:
            self.connected_to_room = False
        return res['success']  # rn no way to fail?

    async def list_rooms(self) -> List[Dict[str, Any]]:
        """
        Asks server for a list of rooms that the current user has joined.

        Returns list of connected rooms.
        Authentication required. Operation cannot fail.
        """
        res = await self._send("listrooms", {})
        return res['servers']
