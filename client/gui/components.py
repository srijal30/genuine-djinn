from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from app import ChatApp
    from tkinter import Misc

import ttkbootstrap as tkb  # type: ignore

__app__ = ("Message",)


class Message(tkb.Label):
    """Message class."""

    def __init__(self, container: Misc, master: ChatApp, msg: Dict[str, Any]):
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
            font=("Sans Serif", 11)
        )

    def set_msg(self, msg: Dict[str, Any]) -> None:
        """Updates the message object."""
        self.msg_data = msg
        if self.msg_data['author']['id'] == 0 or self.msg_data['author']['tag'] == 0:
            self.msg = self.msg_data['content']
        else:
            self.msg = f"{self.msg_data['author']['name']}: {self.msg_data['content']}"
        self.setup()
