import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Event

import ttkbootstrap as tkb  # type: ignore
from ttkbootstrap.scrolled import ScrolledText

__app__ = (
    "ChatFrame",
    "ConnectionFrame",
    "LoginFrame",
    "TestFrame"
)


class ChatFrame(tkb.Frame):
    """Frame for chat page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        # ScrolledText frame
        self.chat_frame = tkb.Frame(master)
        self.chat_frame.grid(row=0, column=0, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)
        self.chat_frame.rowconfigure(0, weight=1)
        self.chat_frame.columnconfigure(0, weight=1)

        self.chat_box = ScrolledText(self.chat_frame, bootstyle="round")
        self.chat_box.text.configure(state="disable")
        self.chat_box.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

        # Entry and Button frame
        self.message_frame = tkb.Frame(master)
        self.message_frame.grid(row=1, column=0, padx=3, pady=3, sticky=tk.W+tk.E)
        self.message_frame.columnconfigure(0, weight=1)

        self.message_box = tkb.Entry(self.message_frame, bootstyle="secondary")
        self.message_box.configure(textvariable=tk.StringVar(value=""))
        self.message_box.grid(row=0, column=0, padx=2, sticky=tk.W+tk.E)
        self.message_box.bind("<Return>", self.on_send)

        self.send_btn = tkb.Button(self.message_frame)
        self.send_btn.configure(text="Send")
        self.send_btn.bind("<ButtonPress>", self.on_send)
        self.send_btn.grid(row=0, column=1, padx=2)

    def on_send(self, event: Event) -> None:
        """On send button or enter press."""
        msg = self.message_box.get().strip()

        if len(msg) > 0:
            self.master.send_message(msg)
            self.message_box.delete(0, "end")

    def display_message(self, message: str) -> None:
        """Displays message in chat."""
        self.chat_box.text.configure(state="normal")
        self.chat_box.text.insert("end", f"{message}\n")
        self.chat_box.text.configure(state="disable")
        self.chat_box.text.yview_moveto(1)

    def clear_chat(self) -> None:
        """Clears contents of the ScrolledText chat."""
        self.chat_box.text.configure(state="normal")
        self.chat_box.text.delete('1.0', "end")
        self.chat_box.text.configure(state="disable")


class ConnectFrame(tkb.Frame):
    """Frame for connect page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.room_label = ttk.Label(self)
        self.room_label.configure(text="Make Room")
        self.room_label.grid(column=0, row=0)

        self.room_box = ttk.Entry(self)
        self.room_box.grid(column=0, padx=20, pady=5, row=1, sticky="w")
        self.room_box.bind("<Return>", self.on_create)

        self.room_btn = ttk.Button(self)
        self.room_btn.configure(text="Create")
        self.room_btn.bind("<ButtonPress>", self.on_create)
        self.room_btn.grid(column=0, pady=3, row=2)

        self.join_label = ttk.Label(self)
        self.join_label.configure(text="Join Room")
        self.join_label.grid(column=2, row=0)

        self.join_box = ttk.Entry(self)
        self.join_box.grid(column=2, padx=20, pady=5, row=1)
        self.join_box.bind("<Return>", self.on_join)

        self.join_btn = ttk.Button(self)
        self.join_btn.configure(text="Join")
        self.join_btn.bind("<ButtonPress>", self.on_join)
        self.join_btn.grid(column=2, pady=3, row=2)

        self.grid_anchor("center")
        self.grid(column=0, columnspan=3, row=0, rowspan=3, sticky=tk.NSEW)

    def on_create(self, event: Event) -> None:
        """On Create Room button press."""
        print("create")

    def on_join(self, event: Event) -> None:
        """On Join Room button press."""
        print("join")


class LoginFrame(tkb.Frame):
    """Frame for login page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.username_label = tkb.Label(self)
        self.username_label.configure(text="Username")
        self.username_label.grid(column=0, padx=5, row=0, sticky="e")

        self.username_box = tkb.Entry(self)
        self.username_box.grid(column=1, ipadx=10, pady=3, row=0, sticky="w")
        self.username_box.bind("<Return>", self.on_login)

        self.password_label = tkb.Label(self)
        self.password_label.configure(text="Password")
        self.password_label.grid(column=0, padx=5, row=1, sticky="e")

        self.password_box = tkb.Entry(self, show="*")
        self.password_box.grid(column=1, ipadx=10, pady=3, row=1, sticky="w")
        self.password_box.bind("<Return>", self.on_login)

        self.login_btn = tkb.Button(self)
        self.login_btn.configure(text="Login")
        self.login_btn.bind("<ButtonPress>", self.on_login)
        self.login_btn.grid(column=0, columnspan=2, pady=15, row=3, sticky="nsew")

        self.grid_anchor("center")
        self.grid(column=0, columnspan=2, row=0, rowspan=3, sticky=tk.NSEW)

    def on_login(self, event: Event) -> None:
        """On login button press."""
        print("login")


class TestFrame(tkb.Frame):
    """Frame for testing and creating."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)
        pass
