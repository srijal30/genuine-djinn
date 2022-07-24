import tkinter as tk
from typing import Union

from frames import ChatFrame, ConnectionFrame, LoginFrame

__all__ = (
    "ChatApp"
)


class ChatApp(tk.Tk):
    """Main chat application window."""

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class: Union[ChatFrame, ConnectionFrame, LoginFrame]) -> None:
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.grid_forget()
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

    async def send_message(self) -> None:
        """Passes a message on to the client server."""
        print("message sent") #DEBUG
        pass

    async def recieve_message(self) -> None:
        """Called by client when a message is recieved."""
        print("message received") #DEBUG
        pass
