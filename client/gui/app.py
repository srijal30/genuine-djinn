import tkinter as tk
from typing import Union

import ttkbootstrap as tkb  # type: ignore
from frames import ChatFrame, ConnectionFrame, LoginFrame
from menus import MainMenu

__all__ = (
    "ChatApp"
)


class ChatApp(tk.Tk):
    """Main chat application window."""

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(ChatFrame)
        tkb.Style("flatly")
        self.config(menu=MainMenu(self))
        self.configure(height=200, width=200)
        self.geometry("800x600")
        self.minsize(400, 300)
        self.resizable(True, True)
        self.title("Chat App")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, uniform=0, weight=1)

    def switch_frame(self, frame_class: Union[ChatFrame, ConnectionFrame, LoginFrame]) -> None:
        """Frame switcher."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

    async def send_message(self) -> None:
        """Passes a message on to the client server."""
        pass

    async def recieve_message(self) -> None:
        """Called by client when a message is recieved."""
        pass
