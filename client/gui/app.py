import asyncio
import threading
from typing import Any, Dict, Union

import ttkbootstrap as tkb  # type: ignore
from client.connection import SocketClient
from frames import ChatFrame, ConnectFrame, LoginFrame, TestFrame
from menus import DebugMenu

__all__ = (
    "ChatApp",
)


class ChatApp(tkb.Window):
    """Main chat application window."""

    currentThread = None

    def __init__(self):
        tkb.Window.__init__(self)

        # window config
        self.configure(height=200, width=200)
        self.geometry("800x600")
        self.minsize(400, 300)
        self.resizable(True, True)
        self.config(menu=DebugMenu(self))  # assign menu for window (MainMenu/DebugMenu)

        # frame switching and buffering
        self.current_frame = None
        self.buffer = {}

        # create SocketClient which will handle all communication b/w client & server
        self.connection = SocketClient()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connection.connect())

        self.switch_frame(LoginFrame)  # starting frame

    def switch_frame(
        self,
        frame: Union[ChatFrame, LoginFrame, ConnectFrame, TestFrame],
        use_old: bool = False
    ) -> None:
        """Switches to provided frame."""
        name = frame.__name__

        if self.current_frame is None or not isinstance(self.current_frame, frame) or use_old:
            if name in self.buffer.items() and self.buffer[name] is not None and not use_old:
                self.buffer[name].destroy()

            self.buffer[name] = frame(self)
            self.current_frame = self.buffer[name]
            self.buffer[name].grid()

    def send_message(self, message: str) -> None:
        """Passes a message on to the client server."""
        # add error handling in the future
        loop = asyncio.get_event_loop()
        self.receive_message({'author': {'name': 'me'}, 'content': message})  # DEBUG
        sucess = loop.run_until_complete(self.connection.send_message(message))
        print(sucess)

    def receive_message(self, message_data: Dict[str, Any]) -> None:
        """Called by client when a message is received."""
        message = f"{message_data['author']['name']}: {message_data['content']}"
        self.buffer[ChatFrame.__name__].display_message(message)

    def start_receiving(self):
        """Starts message receiving thread."""
        receive_coroutine = self.connection.receive_messages(self.receive_message)

        def test():
            loop = asyncio.new_event_loop()
            loop.run_until_complete(receive_coroutine)

        receive_thread = threading.Thread(target=test)
        self.current_thread = receive_thread
        receive_thread.start()
        print("started receiving messages")  # DEBUG

    def stop_receiving(self):
        """Stops the current message receiving thread."""
        if not self.current_thread:
            raise('No thread to stop receiving messages from')
        self.current_thread.join()
        self.current_thread = None
        print("stopped receiving messages")  # DEBUG
