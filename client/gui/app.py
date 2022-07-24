import tkinter as tk
from typing import Union

from frames import ChatFrame, ConnectFrame, LoginFrame, TestFrame
from menus import DebugMenu

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
            "Connect": None,
            "Test": None,
        }

        self.chat_frame()  # starting frame

    def switch_frame(
        self,
        frame: Union[ChatFrame, LoginFrame, ConnectFrame],
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
        if type(self.current_frame) is not ChatFrame or use_old is True or self.current_frame is None:
            self.title("Chat App - Chat")

            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.config(menu=DebugMenu(self))

            # switch frame
            self.switch_frame(ChatFrame, "Chat", use_old)

    def login_frame(self, use_old: bool = False) -> None:
        """Class LoginFrame switching logic and styling."""
        # top level config
        if type(self.current_frame) is not LoginFrame or use_old is True or self.current_frame is None:
            self.title("Chat App - Login")

            self.grid_anchor("center")
            self.config(menu=DebugMenu(self))

            # switch frame
            self.switch_frame(LoginFrame, "Login", use_old)

    def connect_frame(self, use_old: bool = False) -> None:
        """Class ConnectFrame switching logic and styling."""
        # top level config
        if type(self.current_frame) is not ConnectFrame or use_old is True or self.current_frame is None:
            self.title("Chat App - Connect")

            self.grid_anchor("center")
            self.config(menu=DebugMenu(self))

            # switch frame
            self.switch_frame(ConnectFrame, "Connect", use_old)

    def test_frame(self, use_old: bool = False) -> None:
        """Class TestFrame switching logic and styling."""
        # top level config
        if type(self.current_frame) is not TestFrame or use_old is True or self.current_frame is None:
            self.title("Chat App - Test")

            self.config(menu=DebugMenu(self))

            # switch frame
            self.switch_frame(TestFrame, "Connect", use_old)

    def send_message(self, message: str) -> None:
        """Passes a message on to the client server."""
        # self message loop until client server is integrated
        self.receive_message(message)

    def receive_message(self, message: str) -> None:
        """Called by client when a message is received."""
        # needs client integration, currently looping chat messages
        self.buffer["Chat"].display_message(message)
