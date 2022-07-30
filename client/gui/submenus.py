import asyncio
import sys
from tkinter import Menu

import ttkbootstrap as tkb  # type: ignore
from frames import (
    ChatFrame, ConnectFrame, LoginFrame, RegisterFrame, TestFrame
)

__app__ = (
    "FileMenu",
    "ViewMenu",
    "HelpMenu",
    "TestMenu"
)


class FileMenu(tkb.Menu):
    """File dropdown menu."""

    def __init__(self, parent, master):
        tkb.Menu.__init__(self, parent)

        self.master = master

        self.add_command(label="Leave Room", command=self.on_leave)
        self.add_command(label="Log Out", command=self.on_logout)
        self.add_separator()
        self.add_command(label="Quit", command=self.on_quit)

    def on_leave(self) -> None:
        """On Leave Room item press."""
        # ADD FUNC
        pass

    def on_logout(self) -> None:
        """On Log Out item press."""
        loop = self.master.loop
        task = loop.create_task(self.master.connection.logout())

        # POPUP
        def callback(result: asyncio.Task) -> None:
            print("logged out!")
            self.master.switch_frame(LoginFrame)

        task.add_done_callback(callback)

    def on_quit(self) -> None:
        """On Quit item press."""
        self.master.loop.stop()  # end the loop
        sys.exit(0)


class ViewMenu(tkb.Menu):
    """View dropdown menu."""

    def __init__(self, parent, master):
        tkb.Menu.__init__(self, parent)

        self.master = master
        self.parent = parent

        tkb.Style("superhero")  # default theme

        # Clear Chat
        self.add_command(label="Clear Chat", command=self.on_clear)
        self.add_separator()

        # Theme submenu
        theme_menu = Menu(self, tearoff=False)
        theme_menu.add_radiobutton(label="Light", command=self.on_light_mode)
        theme_menu.add_radiobutton(label="Classic", command=self.on_classic_mode)
        theme_menu.add_radiobutton(label="Dark", command=self.on_dark_mode)
        self.add_cascade(label="Theme", menu=theme_menu)

    def on_light_mode(self):
        """Change theme to light mode."""
        tkb.Style("flatly")

    def on_classic_mode(self):
        """Change theme to classic mode."""
        tkb.Style("superhero")

    def on_dark_mode(self):
        """Change theme to dark mode."""
        tkb.Style("darkly")

    def on_clear(self) -> None:
        """On Clear Chat item press."""
        self.master.current_frame.clear_chat()


class HelpMenu(tkb.Menu):
    """Help dropdown menu."""

    def __init__(self, parent, master):
        tkb.Menu.__init__(self, parent)

        self.add_command(label="About", command=self.on_about)

    def on_about(self) -> None:
        """Open About window."""
        about = tkb.Window()
        about.title("Glitchat - About")
        about.minsize(400, 200)
        about_text = tkb.Label(
            about,
            text="https://github.com/srijal30/genuine-djinn"
        )
        about_text.pack()
        about.mainloop()


class TestMenu(tkb.Menu):
    """Debug dropdown menu."""

    def __init__(self, parent, master):
        tkb.Menu.__init__(self, parent)

        self.master = master
        self.parent = parent

        # Frames submenu
        frames_menu = Menu(self, tearoff=False)
        frames_menu.add_command(label="LoginFrame", command=self.login_frame)
        frames_menu.add_command(label="RegisterFrame", command=self.register_frame)
        frames_menu.add_command(label="ConnectFrame", command=self.connect_frame)
        frames_menu.add_command(label="ChatFrame", command=self.chat_frame)
        frames_menu.add_command(label="TestFrame", command=self.test_frame)
        self.add_cascade(label="Frames", menu=frames_menu)

    def login_frame(self) -> None:
        """Switch to LoginFrame"""
        self.master.switch_frame(LoginFrame)

    def register_frame(self) -> None:
        """Switch to LoginFrame"""
        self.master.switch_frame(RegisterFrame)

    def connect_frame(self) -> None:
        """Switch to LoginFrame"""
        self.master.switch_frame(ConnectFrame)

    def chat_frame(self) -> None:
        """Switch to LoginFrame"""
        self.master.switch_frame(ChatFrame)

    def test_frame(self) -> None:
        """Switch to LoginFrame"""
        self.master.switch_frame(TestFrame)
