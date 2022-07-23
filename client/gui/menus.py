import tkinter as tk

import submenus as submenu
import ttkbootstrap as tkb  # type: ignore

__app__ = (
    "MainMenu",
    "DebugMenu"
)


class MainMenu(tk.Menu):
    """Default navigation menu."""

    def __init__(self, master):
        tkb.Menu.__init__(self, master)

        self.add_cascade(label="File", menu=submenu.FileMenu(self))    # File menu
        self.add_cascade(label="View", menu=submenu.ViewMenu(self))    # View menu
        self.add_cascade(label="Help", menu=submenu.HelpMenu(self))    # Help menu


class DebugMenu(tk.Menu):
    """Menu for debugging."""

    def __init__(self, master):
        tkb.Menu.__init__(self, master)

        self.add_cascade(label="File", menu=submenu.FileMenu(self))    # File menu
        self.add_cascade(label="View", menu=submenu.ViewMenu(self))    # View menu
        self.add_cascade(label="Help", menu=submenu.HelpMenu(self))    # Help menu
        self.add_cascade(label="Debug", menu=submenu.DebugMenu(self))  # Debug menu
