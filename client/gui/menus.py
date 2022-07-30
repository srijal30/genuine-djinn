from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

import ttkbootstrap as tkb  # type: ignore
from submenus import FileMenu, HelpMenu, TestMenu, ViewMenu

if TYPE_CHECKING:
    from app import ChatApp

__app__ = ("MainMenu", "DebugMenu")


class MainMenu(tk.Menu):
    """Default navigation menu."""

    def __init__(self, master: ChatApp):
        tkb.Menu.__init__(self, master)

        self.add_cascade(label="File", menu=FileMenu(self, master))  # File menu
        self.add_cascade(label="View", menu=ViewMenu(self, master))  # View menu


class DebugMenu(tk.Menu):
    """Menu for debugging."""

    def __init__(self, master: ChatApp):
        tkb.Menu.__init__(self, master)

        self.add_cascade(label="File", menu=FileMenu(self, master))  # File menu
        self.add_cascade(label="View", menu=ViewMenu(self, master))  # View menu
        self.add_cascade(label="Help", menu=HelpMenu(self, master))  # Help menu
        self.add_cascade(label="Debug", menu=TestMenu(self, master))  # Debug menu
