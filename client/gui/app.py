import asyncio
from typing import Any, Dict, Union

import ttkbootstrap as tkb  # type: ignore
from connection import SocketClient
from frames import (
    ChatFrame, ConnectFrame, LoginFrame, RegisterFrame, TestFrame
)
from menus import DebugMenu

__all__ = ("ChatApp",)


class ChatApp(tkb.Window):
    """Main chat application window."""

    def __init__(self, loop):
        tkb.Window.__init__(self)

        # setup the event loop
        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.close_loop)

        # setup the client
        self.connection = SocketClient()
        loop.run_until_complete(self.connection.connect())

        # room list
        self.room_list = dict()

        # user and tag
        self.user = None
        self.tag = None

        # window config
        self.configure(height=200, width=200)
        self.geometry("800x600")
        self.minsize(800, 600)
        self.resizable(True, True)
        self.config(menu=DebugMenu(self))  # assign menu for window (MainMenu/DebugMenu)

        # frame switching and buffering
        self.current_frame = None
        self.buffer = {}
        self.switch_frame(LoginFrame)  # starting frame

    def switch_frame(
        self,
        frame: Union[ChatFrame, LoginFrame, ConnectFrame, RegisterFrame, TestFrame],
        use_old: bool = False,
    ) -> None:
        """Switches to provided frame."""
        name = frame.__name__

        if (
            self.current_frame is None
            or not isinstance(self.current_frame, frame)
            or use_old
        ):
            if (
                name in self.buffer.items()
                and self.buffer[name] is not None
                and not use_old
            ):
                self.buffer[name].destroy()

            self.buffer[name] = frame(self)
            self.current_frame = self.buffer[name]
            self.buffer[name].grid()

    def send_message(self, message: str) -> None:
        """Passes a message on to the client server."""
        # add error handling in the future
        self.receive_message({"author": {"name": "me"}, "content": message})  # DEBUG
        task = self.loop.create_task(self.connection.send_message(message))

        def callback(result: asyncio.Future) -> None:
            success = result.result()
            print(success)

        task.add_done_callback(callback)

    def receive_message(self, message_data: Dict[str, Any]) -> None:
        """Called by client when a message is received."""
        self.buffer[ChatFrame.__name__].display_message(message_data)

    def receive_room_list(self, room_list) -> None:
        """Grabs roomlist from client socket."""
        # calling this should return the list of rooms from the client
        self.room_list = room_list

    def update_loop(self) -> None:
        """Updates the GUI through the asyncio event loop."""
        self.update()
        self.loop.call_soon(self.update_loop)

    def close_loop(self) -> None:
        """Closes the asyncio event loop."""
        self.loop.stop()
