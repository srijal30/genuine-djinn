import json
import random
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

import websockets

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from enhancers.message_processer import (  # noqa: E402
    AutoCorrecter, AutoTranslater
)

# TO DO LIST:
# - allow user to choose domain in GUI
# - add message history endpoint
# - make sure message listener shows 'stopped receiving'

# ADD
DOMAIN = "ws://192.155.88.143:5005"
# DOMAIN = "ws://localhost:5000"
ROUTE = "/ws"
URL = DOMAIN + ROUTE

autocorrecter = AutoCorrecter()
autotranslater = AutoTranslater()


# add what ip to connect to in the constructor?
# add a __new__ method so that we can call connect on construction
class SocketClient:
    """API Wrapper that handles all client side communication with the server."""

    connected_to_room = False  # is this required?

    async def connect(self):
        """Connects to the server. Must be called in order for everything to work."""
        self.ws = await websockets.connect(URL)
        print("connected!")  # DEBUG

    async def _receive(self) -> Dict[str, Any]:
        """Receives a message from the server. Converts raw data to python dict."""
        res = await self.ws.recv()
        load = json.loads(res)

        return load

    async def _send(
        self, type: str, payload: Dict[str, Any], reply: bool = True
    ) -> Dict[str, Any]:
        """Sends a message to the server. Expects no reply by default."""
        req = json.dumps({"type": type, **payload})
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
        payload = {"username": username, "tag": tag, "password": password}
        res = await self._send("login", payload)
        return res["success"]

    async def logout(self) -> bool:
        """
        Logs out the user.

        Returns if successful or not.
        """
        res = await self._send("logout", {})
        return res["success"]

    async def register(self, username: str, password: str) -> int:
        """
        Sends a register request to the server. Also logs user in.

        Returns the unique user tag of the new user.
        """
        payload = {"username": username, "password": password}
        res = await self._send("register", payload)
        return res["tag"]

    async def create_room(self, name: str) -> Tuple[int, int]:
        """
        Asks the server to create a room with given name. Also joins room.

        Returns (roomcode, roomid) of the newly created room.
        Cannot fail. Authentication is required.
        """
        payload = {"name": name}
        res = await self._send("createroom", payload)
        return (res["code"], res["id"])

    async def join_room(self, code: str) -> Dict[str, Any]:
        """
        Joins the room with given code.

        Returns the room information of newly joined room.
        Authentication required.
        """
        payload = {"code": code}
        res = await self._send("joinroom", payload)
        return res

    async def connect_room(self, id: int) -> bool:
        """
        Connects to a room.

        Returns whether connection was successful or not.
        Authentication required. Joining room required.
        """
        payload = {"id": id}
        res = await self._send("roomconnect", payload)
        self.connected_to_room = res["success"]
        return res["success"]

    # check what msg is, is it a json or string???
    async def message_listener(self, callback: Callable[[str], None]) -> None:
        """
        Starts a message receiving listener.

        When a message is received, callback function is called on the new message.
        Authentication required. Connected room required.
        """
        async for res in self.ws:
            # makes sure that there is a way for loop to end
            if not self.connected_to_room:
                print("stopped receicving")  # see if we even neee Task.cancel()
                break
            res = json.loads(res)
            # if not a roomconnect message, then break
            if res["type"] != "roomconnect":
                break
            # edited message or new message
            if "new" in res:
                msg = res["new"]
                callback(msg)  # make this the new_callback
            else:
                msg = res["update"]
                # update_callback(msg)

        print("stopped receiving")  # DEBUG

    async def send_message(self, message: str) -> bool:
        """
        Sends a message to the server.

        Does not expect a reply from the server.
        Authentication required. Connected room required.
        """
        enhanced_message = message
        if "*" not in [message[0], message[-1]]:
            random_enhancer = random.choice(
                [
                    autocorrecter.autocorrect_string,
                    autocorrecter.autocorrect_entities,
                    autotranslater.auto_translate_to_owoify,
                    autotranslater.auto_translate_to_boomhauer,
                    autotranslater.auto_translate_to_pig_latin,
                ]
            )
            enhanced_message = random_enhancer(message)
            print("Enhanced Message: ", enhanced_message)
        payload = {"content": enhanced_message, "action": "send"}
        # payload = {"content": message, "action": "send"}
        await self._send("roomconnect", payload, reply=False)
        return True  # rn no way to fail?

    async def exit_room(self) -> bool:
        """
        Exits the currently connected room.

        Returns whether succesful or not.
        Authentication required. Connected room required.
        """
        payload = {"end": True}
        await self._send("roomconnect", payload, reply=False)
        self.connected_to_room = False
        return True

    async def list_rooms(self) -> List[Dict[str, Any]]:
        """
        Asks server for a list of rooms that the current user has joined.

        Returns list of connected rooms.
        Authentication required. Operation cannot fail.
        """
        res = await self._send("listrooms", {})
        return res["servers"]

    async def change_name(self, new_name: str) -> bool:
        """
        Asks the server to change currently logged in users name.

        Returns whether successful or not.
        Authentication required.
        """
        payload = {"name": new_name}
        res = await self._send("changename", payload)
        return res["success"]

    async def leave_room(self, id: int) -> bool:
        """
        Unjoins the room with specified id.

        Returns whether successful or not.
        Authentication required. Must have already joined the room.
        """
        payload = {"id": id}
        res = await self._send("leaveroom", payload)
        return res["success"]
