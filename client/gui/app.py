import asyncio
from typing import Any, Dict, List, Type, Union

import ttkbootstrap as tkb  # type: ignore
from connection import SocketClient
from frames import (
    ChatFrame, ConnectFrame, LoginFrame, RegisterFrame, TestFrame
)
from menus import MainMenu
from ttkbootstrap.dialogs.dialogs import Messagebox as msgbox

__all__ = ("ChatApp",)

Frame = Union[
    ChatFrame,
    LoginFrame,
    ConnectFrame,
    RegisterFrame,
    TestFrame,
]


class ChatApp(tkb.Window):
    """Main chat application window."""

    def __init__(self, loop: asyncio.AbstractEventLoop):
        tkb.Window.__init__(self)

        # setup the event loop
        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.close_loop)

        # ADD CODE SO THAT BEFORE CONNECTING AN IP IS PROVIDED (maybe create new input box/ function for connectio)
        # setup the client
        self.connection = SocketClient()
        loop.run_until_complete(self.connection.connect())

        # room list
        self.room_list: List[dict] = []
        self.current_room = None

        # user and tag
        self.user = None
        self.tag = None

        # window config
        self.configure(height=200, width=200)
        self.geometry("800x600")
        self.minsize(800, 600)
        self.resizable(True, True)
        self.config(menu=MainMenu(self))  # assign menu for window (MainMenu/DebugMenu)

        # frame switching and buffering
        self.current_frame = None
        self.buffer: Dict[str, Frame] = {}
        self.switch_frame(LoginFrame)  # starting frame

    def switch_frame(
        self,
        frame: Type[Frame],
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
        task = self.loop.create_task(self.connection.send_message(message))

        def callback(result: asyncio.Task) -> None:
            success = result.result()
            print(success)

        task.add_done_callback(callback)

    def popup(self, type: str, message: str):
        """Creates a popup message in the app. Type can be either 'error' or 'success'"""
        match type.lower():
            case "error":
                msgbox.show_error(
                    message=message,
                    title='An Error Has Occured',
                    parent=self,
                    alert=True
                )
            case "success":
                msgbox.show_info(
                    message=message,
                    title='Success',
                    parent=self,
                    alert=False
                )
            case "about":
                msgbox.ok(
                    message=message,
                    title='About',
                    parent=self,
                    alert=False
                )

    def receive_message(self, message_data: Dict[str, Any]) -> None:
        """Called by client when a message is received."""
        # check if it is a system message
        self.buffer[ChatFrame.__name__].display_message(message_data)  # type: ignore
        # ???

    # calling this should return the list of rooms from the client
    async def get_room_list(self) -> None:
        """Updates room_list with latest data from the server."""
        # task = self.loop.create_task(self.connection.list_rooms())
        self.room_list = await self.connection.list_rooms()

    def update_loop(self) -> None:
        """Updates the GUI through the asyncio event loop."""
        self.update()
        self.loop.call_soon(self.update_loop)

    def close_loop(self) -> None:
        """Closes the asyncio event loop."""
        self.loop.stop()
