from __future__ import annotations

import asyncio
import sys
from tkinter import Menu, Misc
from typing import TYPE_CHECKING

import ttkbootstrap as tkb  # type: ignore
from frames import (
    ChatFrame, ConnectFrame, LoginFrame, RegisterFrame, TestFrame
)

if TYPE_CHECKING:
    from app import ChatApp

__app__ = ("FileMenu", "ViewMenu", "HelpMenu", "TestMenu")


class FileMenu(tkb.Menu):
    """File dropdown menu."""

    def __init__(self, parent: Misc, master: ChatApp):
        tkb.Menu.__init__(self, parent)

        self.master: ChatApp = master

        self.add_command(label="Leave Room", command=self.on_leave)
        self.add_command(label="Log Out", command=self.on_logout)
        self.add_separator()
        self.add_command(label="Quit", command=self.on_quit)

    def on_leave(self) -> None:
        """On Leave Room item press."""
        if self.master.current_room is None:
            self.master.popup('error', 'You must be in a room in order to leave it!')
            return

        loop = self.master.loop
        task = loop.create_task(self.master.connection.exit_room())

        def callback(result: asyncio.Task):
            self.master.current_room = None

        task.add_done_callback(callback)

    def on_logout(self) -> None:
        """On Log Out item press."""
        # check if in a room currently
        if self.master.current_room:
            self.master.popup('error', 'You must not be connected to any rooms in order to logout!')
            return

        # check if we are even logged in
        if not self.master.user and not self.master.tag:
            self.master.popup('error', 'You must be logged in to logout!')
            return

        self.master.user = None
        self.master.tag = None

        loop = self.master.loop
        task = loop.create_task(self.master.connection.logout())

        # POPUP
        def callback(result: asyncio.Task) -> None:
            self.master.switch_frame(LoginFrame)
            self.master.popup('success', 'You have successfully logged out!')

        task.add_done_callback(callback)

    def on_quit(self) -> None:
        """On Quit item press."""
        self.master.loop.stop()  # end the loop
        sys.exit(0)


class ViewMenu(tkb.Menu):
    """View dropdown menu."""

    def __init__(self, parent: Misc, master: ChatApp) -> None:
        tkb.Menu.__init__(self, parent)

        self.master: ChatApp = master
        self.parent = parent

        tkb.Style("darkly")  # default theme

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
        if type(self.master.current_frame) != ChatFrame:
            self.master.popup('error', 'You can only clear chat when connected to a chatroom!')
            return
        self.master.current_frame.clear_chat()


class HelpMenu(tkb.Menu):
    """Help dropdown menu."""

    def __init__(self, parent: Misc, master: ChatApp):
        tkb.Menu.__init__(self, parent)

        self.master: ChatApp = master
        self.parent = parent

        self.add_command(label="About", command=self.on_about)

    def on_about(self) -> None:
        """Open About window."""
        self.master.popup(
            type="about",
            message="Glitchat - A Python Summer Code Jam 2022 Project\nhttps://github.com/srijal30/genuine-djinn"
        )


class TestMenu(tkb.Menu):
    """Debug dropdown menu."""

    def __init__(self, parent: Misc, master: ChatApp):
        tkb.Menu.__init__(self, parent)

        self.master: ChatApp = master
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
