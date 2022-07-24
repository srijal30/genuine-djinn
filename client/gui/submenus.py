import sys
import tkinter as tk
from tkinter import IntVar, Menu

import ttkbootstrap as tkb  # type: ignore

__app__ = ("FileMenu", "ViewMenu", "HelpMenu", "DebugMenu")


class FileMenu(tk.Menu):
    """File dropdown menu."""

    def __init__(self, parent, master):
        tkb.Menu.__init__(self, parent)

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

    def __init__(self, parent, master):
        tkb.Menu.__init__(self, parent)

        tkb.Style("darkly")  # flatly/darkly

        # Text Size submenu
        size_menu = Menu(self, tearoff=False)
        size_menu.add_radiobutton(label="Small", value=1, variable=IntVar)
        size_menu.add_radiobutton(label="Medium", value=1, variable=IntVar)
        size_menu.add_radiobutton(label="Large", value=1, variable=IntVar)
        self.add_cascade(label="Text Size", menu=size_menu)

        # Theme submenu
        theme_menu = Menu(self, tearoff=False)
        theme_menu.add_radiobutton(
            label="Light", value=1, variable=IntVar, command=self.on_light_mode
        )
        theme_menu.add_radiobutton(
            label="Dark", value=1, variable=IntVar, command=self.on_dark_mode
        )
        self.add_cascade(label="Theme", menu=theme_menu)

    def on_light_mode(self):
        """Change theme to light mode."""
        tkb.Style("flatly")

    def on_dark_mode(self):
        """Change theme to dark mode."""
        tkb.Style("darkly")


class HelpMenu(tk.Menu):
    """Help dropdown menu."""

    def __init__(self, parent, master):
        tkb.Menu.__init__(self, parent)

        self.add_command(label="About", command=self.on_about)

    def on_about(self) -> None:
        """On About item press."""
        pass


class DebugMenu(tk.Menu):
    """Debug dropdown menu."""

    def __init__(self, parent, master):
        tkb.Menu.__init__(self, parent)

        # Frames submenu
        frames_menu = Menu(self, tearoff=False)
        frames_menu.add_command(label="LoginFrame", command=master.login_frame)
        frames_menu.add_command(label="ConnectFrame", command=master.connect_frame)
        frames_menu.add_command(label="ChatFrame", command=master.chat_frame)
        self.add_cascade(label="Frames", menu=frames_menu)
