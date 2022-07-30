from typing import Any, Dict

import ttkbootstrap as tkb  # type: ignore

__app__ = (
    "Message",
    "Room"
)


class Message(tkb.Label):
    """Message class."""

    def __init__(self, container, master, msg: Dict[str, Any]):
        tkb.Label.__init__(self, container)

        self.msg_data = msg
        self.container = container
        self.master = master

        self.msg = f"{self.msg_data['author']['name']}: {self.msg_data['content']}"
        self.setup()

    def setup(self) -> None:
        """Configure the Label object."""
        self.config(
            text=self.msg,
            justify="left",
            wraplength=self.master.winfo_width() * 0.75,
        )

    def set_msg(self, msg: Dict[str, Any]) -> None:
        """Updates the message object."""
        self.msg_data = msg
        self.msg = f"{self.msg_data['author']['name']}: {self.msg_data['content']}"
        self.setup()


class Room:
    """Room class."""

    def __init__(self, room_class):
        # self.chat_class = chat_class
        self.room = room_class
