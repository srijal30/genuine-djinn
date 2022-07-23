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

        self.chat_box = ScrolledText(self)
        self.chat_box.configure(state="disabled")
        self.chat_box.grid(column=0, columnspan=2, row=0, rowspan=1, sticky=tk.NSEW)

        self.message_box = tkb.Entry(self)
        self.message_box.configure(textvariable=tk.StringVar(value=""))
        self.message_box.grid(column=0, padx=3, pady=5, row=1, rowspan=1, sticky=tk.NSEW)
        self.message_box.bind("<Return>", self.on_enter, add="")

        self.send_btn = tkb.Button(self)
        self.send_btn.configure(text="Send", command=self.on_send)
        self.send_btn.grid(column=1, padx=3, pady=5, row=1, rowspan=1, sticky=tk.NSEW)

        self.grid_anchor("center")
        self.grid(column=0, columnspan=2, row=0, rowspan=2, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def on_send(self) -> None:
        """On send button press."""
        print("send")

    def on_enter(self, event: Event) -> None:
        """On enter press in messagebox."""
        print(event)


class ConnectFrame(ttk.Frame):
    """Frame for connect page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)


class LoginFrame(ttk.Frame):
    """Frame for login page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.username_label = tkb.Label(self)
        self.username_label.configure(text="Username")
        self.username_label.grid(column=0, padx=5, row=0, sticky="e")
        self.username_box = tkb.Entry(self)
        self.username_box.grid(column=1, ipadx=10, pady=3, row=0, sticky="w")
        self.password_label = tkb.Label(self)
        self.password_label.configure(text="Password")
        self.password_label.grid(column=0, padx=5, row=1, sticky="e")
        self.password_box = tkb.Entry(self, show="*")
        self.password_box.grid(column=1, ipadx=10, pady=3, row=1, sticky="w")
        self.login_btn = tkb.Button(self)
        self.login_btn.configure(text="Login")
        self.login_btn.bind("<ButtonPress>", self.on_login)
        self.login_btn.grid(column=0, columnspan=2, pady=15, row=3, sticky="nsew")

        self.grid_anchor("center")
        self.grid(column=0, columnspan=2, row=0, rowspan=3, sticky=tk.NSEW)

    def reset(self) -> None:
        """Reset the frame."""
        pass

    def on_login(self, event: Event = None) -> None:
        """On login button press."""
        pass
