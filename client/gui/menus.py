import sys
import tkinter as tk
from tkinter import IntVar, Menu

import ttkbootstrap as tkb  # type: ignore

__app__ = (
    "MainMenu"
)


class MainMenu(tk.Menu):
    """Main navigation menu."""

    def __init__(self, master):
        tkb.Menu.__init__(self, master)

        # file menu
        file_menu = Menu(self, tearoff=False)
        file_menu.add_command(label="Leave Room", command=self.on_leave)
        file_menu.add_command(label="Log Out", command=self.on_logout)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.on_quit)
        self.add_cascade(label="File", menu=file_menu)

        # edit menu
        view_menu = Menu(self, tearoff=False)

        size_menu = Menu(view_menu, tearoff=False)
        size_menu.add_radiobutton(label="Small", value=1, variable=IntVar)
        size_menu.add_radiobutton(label="Medium", value=1, variable=IntVar)
        size_menu.add_radiobutton(label="Large", value=1, variable=IntVar)
        view_menu.add_cascade(label="Text Size", menu=size_menu)

        theme_menu = Menu(view_menu, tearoff=False)
        theme_menu.add_radiobutton(label="Light", value=1, variable=IntVar)
        theme_menu.add_radiobutton(label="Dark", value=1, variable=IntVar)
        view_menu.add_cascade(label="Theme", menu=theme_menu)

        self.add_cascade(label="View", menu=view_menu)

        # help menu
        helpmenu = Menu(self, tearoff=False)
        helpmenu.add_command(label="About", command=self.on_about)
        self.add_cascade(label="Help", menu=helpmenu)

    def on_leave(self) -> None:
        """On Leave Room item press."""
        pass

    def on_logout(self) -> None:
        """On Log Out item press."""
        pass

    def on_quit(self) -> None:
        """On Quit item press."""
        sys.exit(0)

    def on_about(self) -> None:
        """On About item press."""
        pass
