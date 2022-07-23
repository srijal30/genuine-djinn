import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Event
from tkinter.scrolledtext import ScrolledText

import ttkbootstrap as tkb  # type: ignore

# from ttkbootstrap.constants import DARK

__app__ = (
    "ChatFrame",
    "ConnectionFrame",
    "LoginFrame"
)


class ChatFrame(tkb.Frame):
    """Frame for chat page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.chatbox = ScrolledText()
        self.chatbox.configure(state="disabled")
        self.chatbox.grid(column=0, columnspan=2, row=0, rowspan=1, sticky=tk.NSEW)

        self.messagebox = tkb.Entry()
        self.messagebox.configure(textvariable=tk.StringVar(value=""))
        self.messagebox.grid(column=0, padx=3, pady=5, row=1, rowspan=1, sticky=tk.NSEW)
        self.messagebox.bind("<Return>", self.on_enter, add="")

        self.sendbutton = tkb.Button()
        self.sendbutton.configure(text="Send")
        self.sendbutton.grid(column=1, padx=3, pady=5, row=1, rowspan=1, sticky=tk.NSEW)
        self.sendbutton.configure(command=self.on_send)

        self.configure(height=200, padding=5, width=200)
        self.grid_anchor("center")
        self.grid(column=0, columnspan=2, row=0, rowspan=2, sticky=tk.NSEW)

    def on_send(self) -> None:
        """On send button press."""
        print("send")

    def on_enter(self, event: Event) -> None:
        """On enter press in messagebox."""
        print(event)


class ConnectionFrame(ttk.Frame):
    """Frame for connection page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)


class LoginFrame(ttk.Frame):
    """Frame for login page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)
