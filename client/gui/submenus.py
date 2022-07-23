import sys
import tkinter as tk
from tkinter import IntVar, Menu

import ttkbootstrap as tkb  # type: ignore

__app__ = (
    "FileMenu",
    "ViewMenu",
    "HelpMenu",
    "DebugMenu"
)


class FileMenu(tk.Menu):
    """File dropdown menu."""

    def __init__(self, master):
        tkb.Menu.__init__(self, master)

        self.add_command(label="Leave Room", command=self.on_leave)
        self.add_command(label="Log Out", command=self.on_logout)
        self.add_separator()
        self.add_command(label="Quit", command=self.on_quit)

    def on_leave(self) -> None:
        """On Leave Room item press."""
        pass

    def on_logout(self) -> None:
        """On Log Out item press."""
        pass

    def on_quit(self) -> None:
        """On Quit item press."""
        sys.exit(0)


class ViewMenu(tk.Menu):
    """View dropdown menu."""

    def __init__(self, master):
        tkb.Menu.__init__(self, master)

        tkb.Style("darkly")  # flatly/darkly

        # Text Size submenu
        size_menu = Menu(self, tearoff=False)
        size_menu.add_radiobutton(label="Small", value=1, variable=IntVar)
        size_menu.add_radiobutton(label="Medium", value=1, variable=IntVar)
        size_menu.add_radiobutton(label="Large", value=1, variable=IntVar)
        self.add_cascade(label="Text Size", menu=size_menu)

        # Theme submenu
        theme_menu = Menu(self, tearoff=False)
        theme_menu.add_radiobutton(label="Light", value=1, variable=IntVar)
        theme_menu.add_radiobutton(label="Dark", value=1, variable=IntVar)
        self.add_cascade(label="Theme", menu=theme_menu)


class HelpMenu(tk.Menu):
    """Help dropdown menu."""

    def __init__(self, master):
        tkb.Menu.__init__(self, master)

        self.add_command(label="About", command=self.on_about)

    def on_about(self) -> None:
        """On About item press."""
        pass


class DebugMenu(tk.Menu):
    """Debug dropdown menu."""

    def __init__(self, master):
        tkb.Menu.__init__(self, master)

        # Frames submenu
        frames_menu = Menu(self, tearoff=False)
        frames_menu.add_command(label="ChatFrame", command=self.on_frame("Chat"))
        frames_menu.add_command(label="ConnectionFrame", command=self.on_frame("Connection"))
        frames_menu.add_command(label="LoginFrame", command=self.on_frame("Login"))
        self.add_cascade(label="Frames", menu=frames_menu)

    def on_frame(self, frame) -> None:
        """Switch to desired frame."""
        # self.master.switch_frame(frame)
