import tkinter as tk
from typing import Union

import frames as f
import menus as menu

__all__ = (
    "ChatApp"
)


class ChatApp(tk.Tk):
    """Main chat application window."""

    def __init__(self):
        tk.Tk.__init__(self)

        # window config
        self.configure(height=200, width=200)
        self.geometry("800x600")
        self.minsize(400, 300)
        self.resizable(True, True)

        # frame switching and buffering
        self.current_frame = None
        self.buffer = {
            "Chat": None,
            "Login": None,
            "Connect": None
        }

        self.login_frame()  # starting frame

    def switch_frame(
        self,
        frame: Union[f.ChatFrame, f.LoginFrame, f.ConnectFrame],
        name: str,
        use_old: bool = False
    ) -> None:
        """Switches to provided frame."""
        if self.buffer[name] is not None and not use_old:
            self.buffer[name].destroy()

        self.buffer[name] = frame(self)
        self.current_frame = self.buffer[name]
        self.buffer[name].grid()

    def chat_frame(self, use_old: bool = False) -> None:
        """Class ChatFrame switching logic and styling."""
        # top level config
        if type(self.current_frame) is not f.ChatFrame or use_old is True or self.current_frame is None:
            self.title("Chat App - Chat")

            self.grid_anchor("center")
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.config(menu=menu.DebugMenu(self))

            # switch frame
            self.switch_frame(f.ChatFrame, "Chat", use_old)

    def login_frame(self, use_old: bool = False) -> None:
        """Class LoginFrame switching logic and styling."""
        # top level config
        if type(self.current_frame) is not f.LoginFrame or use_old is True or self.current_frame is None:
            self.title("Chat App - Login")

            self.grid_anchor("center")
            self.config(menu=menu.DebugMenu(self))

            # switch frame
            self.switch_frame(f.LoginFrame, "Login", use_old)

    def connect_frame(self, use_old: bool = False) -> None:
        """Class ConnectFrame switching logic and styling."""
        # top level config
        if type(self.current_frame) is not f.ConnectFrame or use_old is True or self.current_frame is None:
            self.title("Chat App - Connect")

            self.grid_anchor("center")
            self.config(menu=menu.DebugMenu(self))

            # switch frame
            self.switch_frame(f.ConnectFrame, "Connect", use_old)

    async def send_message(self) -> None:
        """Passes a message on to the client server."""
        pass

    async def receive_message(self) -> None:
        """Called by client when a message is received."""
        pass
