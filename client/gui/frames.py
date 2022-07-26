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

        self.master = master

        self.master.title("Chat App - Chat")

        self.grid(row=0, rowspan=3, column=0, columnspan=3, padx=3, pady=3, sticky=tkb.NSEW)
        self.menu_subframe = self.MenuSubframe(self, self.master)
        self.chat_subframe = self.ChatSubframe(self, self.master)
        self.entry_subframe = self.EntrySubframe(self, self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    class MenuSubframe(tkb.Frame):
        """Subframe for chat menu."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(row=0, rowspan=1, column=0, columnspan=3, sticky=tkb.NSEW)

            self.room_info = tkb.Label(self.parent)
            self.room_info.configure(text="Room Info")
            self.room_info.grid(row=0, column=0, padx=2, sticky=tkb.NSEW)

            self.menu_btn = tkb.Button(self.parent)
            self.menu_btn.configure(text="Menu")
            self.menu_btn.bind("<ButtonPress>", self.parent.on_menu)
            self.menu_btn.grid(row=0, column=1, padx=2, sticky=tkb.NSEW)

            self.leave_btn = tkb.Button(self.parent)
            self.leave_btn.configure(text="Leave")
            self.leave_btn.bind("<ButtonPress>", self.parent.on_leave)
            self.leave_btn.grid(row=0, column=2, padx=2, sticky=tkb.NSEW)

    class ChatSubframe(tkb.Frame):
        """Subframe for scrolling chat."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(row=1, rowspan=1, column=0, columnspan=3, sticky=tkb.NSEW)

            self.chat_box = ScrolledText(self.parent, bootstyle="round")
            #self.chat_box.text.configure(state="disable")
            self.chat_box.grid(row=1, column=0, columnspan=3, sticky=tkb.NSEW)

    class EntrySubframe(tkb.Frame):
        """Subframe for chat entry and sending."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(row=2, rowspan=1, column=0, columnspan=3, sticky=tkb.NSEW)
            self.columnconfigure(0, weight=1)

            self.message_box = tkb.Entry(self.parent, bootstyle="secondary")
            self.message_box.configure(textvariable=tk.StringVar(value=""))
            self.message_box.grid(row=2, column=0, padx=2, sticky=tkb.NSEW)
            self.message_box.bind("<Return>", self.parent.on_send)

            self.char_btn = tkb.Button(self.parent)
            self.char_btn.configure(text="Emotes")
            self.char_btn.bind("<ButtonPress>", self.parent.on_char)
            self.char_btn.grid(row=2, column=1, padx=2, sticky=tkb.NSEW)

            self.send_btn = tkb.Button(self.parent)
            self.send_btn.configure(text="Send")
            self.send_btn.bind("<ButtonPress>", self.parent.on_send)
            self.send_btn.grid(row=2, column=2, padx=2, sticky=tkb.NSEW)

    def on_send(self, event: Event) -> None:
        """On send button or enter press. Send message."""
        msg = self.entry_subframe.message_box.get().strip()

        if len(msg) > 0:
            print(f"Message: {msg}")
            self.master.send_message(msg)
            self.entry_subframe.message_box.delete(0, "end")

    def on_menu(self, event: Event) -> None:
        """Open chat option menu when button pressed."""
        print("chat menu")

    def on_leave(self, event: Event) -> None:
        """On leave button being pressed. Leave chat room."""
        print("Leave")

    def on_char(self, event: Event) -> None:
        """Open char menu on button click."""
        print("emote/character menu")

    def set_info(self, message: str) -> None:
        """Set message at top of chat room."""
        self.menu_subframe.room_info.configure(text=message)

    def display_message(self, message: str) -> None:
        """Displays message in chat."""
        self.chat_subframe.chat_box.text.configure(state="normal")

        self.label = tk.Label(self.chat_subframe.chat_box, text=message, background='#d0ffff', justify='left', padx=10, pady=5, wraplength=self.master.winfo_width()*0.75) 
        self.chat_subframe.chat_box.insert('end', '\n')
        self.chat_subframe.chat_box.window_create('end', window=self.label)

        #self.chat_subframe.chat_box.text.insert("end", f"{message}\n")
        self.chat_subframe.chat_box.text.configure(state="disable")
        self.chat_subframe.chat_box.text.yview_moveto(1)

    def clear_chat(self) -> None:
        """Clears contents of the ScrolledText chat."""
        self.chat_subframe.chat_box.text.configure(state="normal")
        self.chat_subframe.chat_box.text.delete('1.0', "end")
        self.chat_subframe.chat_box.text.configure(state="disable")


class ConnectFrame(tkb.Frame):
    """Frame for connect page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Connect")

        self.grid_anchor("center")
        self.grid(column=0, columnspan=2, row=0, rowspan=3, padx=3, pady=3, sticky=tkb.NSEW)
        self.join_subframe = self.JoinSubframe(self, self.master)
        self.create_subframe = self.CreateSubframe(self, self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    class JoinSubframe(tkb.Frame):
        """Subframe for joining a room."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(column=0, columnspan=1, row=0, rowspan=3)

            self.join_label = tkb.Label(self.parent)
            self.join_label.configure(text="Join Room")
            self.join_label.grid(column=0, row=0)

            self.join_box = tkb.Entry(self.parent)
            self.join_box.grid(column=0, row=1, padx=20, pady=5)
            self.join_box.bind("<Return>", self.parent.on_join)

            self.join_btn = tkb.Button(self.parent)
            self.join_btn.configure(text="Join")
            self.join_btn.bind("<ButtonPress>", self.parent.on_join)
            self.join_btn.grid(column=0, row=2, pady=3)

    class CreateSubframe(tkb.Frame):
        """Subframe for creating a room."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(column=1, columnspan=1, row=0, rowspan=3)

            self.create_label = tkb.Label(self.parent)
            self.create_label.configure(text="Make Room")
            self.create_label.grid(column=1, row=0)

            self.create_box = tkb.Entry(self.parent)
            self.create_box.grid(column=1, row=1, padx=20, pady=5)
            self.create_box.bind("<Return>", self.parent.on_create)

            self.room_btn = tkb.Button(self.parent)
            self.room_btn.configure(text="Create")
            self.room_btn.bind("<ButtonPress>", self.parent.on_create)
            self.room_btn.grid(column=1, row=2, pady=3)

    def on_create(self, event: Event) -> None:
        """On Create Room button press."""
        print(f"Room Code (Create): {self.create_subframe.create_box.get().strip()}")

    def on_join(self, event: Event) -> None:
        """On Join Room button press."""
        print(f"Room Code (Join): {self.join_subframe.join_box.get().strip()}")


class LoginFrame(tkb.Frame):
    """Frame for login page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Login")

        self.grid_anchor("center")
        self.grid(column=0, columnspan=5, row=0, rowspan=4, sticky=tkb.NSEW)
        self.login_subframe = self.LoginSubframe(self, self.master)
        self.separator = tkb.Separator(self, orient="vertical")
        self.separator.grid(column=2, columnspan=1, row=0, rowspan=4, padx=30, sticky=tkb.NSEW)
        self.register_subframe = self.RegisterSubframe(self, self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    class LoginSubframe(tkb.Frame):
        """Subframe for login form."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid_anchor("center")
            self.grid(column=0, columnspan=2, row=0, rowspan=4, sticky=tkb.NSEW)

            self.login_username_label = tkb.Label(self.parent)
            self.login_username_label.configure(text="Username")
            self.login_username_label.grid(column=0, row=0, sticky=tkb.E)

            self.login_username_box = tkb.Entry(self.parent)
            self.login_username_box.grid(column=1, ipadx=10, padx=5, pady=3, row=0)
            self.login_username_box.bind("<Return>", self.parent.on_login)

            self.login_tag_label = tkb.Label(self.parent)
            self.login_tag_label.configure(text="Tag")
            self.login_tag_label.grid(column=0, row=1, sticky=tkb.E)

            self.login_tag_box = tkb.Entry(self.parent)
            self.login_tag_box.grid(column=1, ipadx=10, padx=5, pady=3, row=1)
            self.login_tag_box.bind("<Return>", self.parent.on_login)

            self.login_password_label = tkb.Label(self.parent)
            self.login_password_label.configure(text="Password")
            self.login_password_label.grid(column=0, row=2, sticky=tkb.E)

            self.login_password_box = tkb.Entry(self.parent, show="*")
            self.login_password_box.grid(column=1, ipadx=10, padx=5, pady=3, row=2)
            self.login_password_box.bind("<Return>", self.parent.on_login)

            self.login_btn = tkb.Button(self.parent)
            self.login_btn.configure(text="Login")
            self.login_btn.bind("<ButtonPress>", self.parent.on_login)
            self.login_btn.grid(column=0, columnspan=2, pady=15, row=3)

    class RegisterSubframe(tkb.Frame):
        """Subframe for registration form."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(column=3, columnspan=2, row=0, rowspan=4, sticky=tkb.NSEW)

            self.register_username_label = tkb.Label(self.parent)
            self.register_username_label.configure(text="Username")
            self.register_username_label.grid(column=3, padx=5, row=0, sticky=tkb.E)

            self.register_username_box = tkb.Entry(self.parent)
            self.register_username_box.grid(column=4, ipadx=10, pady=3, row=0)
            self.register_username_box.bind("<Return>", self.parent.on_register)

            self.register_password_label = tkb.Label(self.parent)
            self.register_password_label.configure(text="Password")
            self.register_password_label.grid(column=3, padx=5, row=1, sticky=tkb.E)

            self.register_password_box = tkb.Entry(self.parent, show="*")
            self.register_password_box.grid(column=4, ipadx=10, pady=3, row=1)
            self.register_password_box.bind("<Return>", self.parent.on_register)

            self.register_btn = tkb.Button(self.parent)
            self.register_btn.configure(text="Register")
            self.register_btn.bind("<ButtonPress>", self.parent.on_register)
            self.register_btn.grid(column=3, columnspan=2, pady=15, row=3)

    def on_login(self, event: Event) -> None:
        """On login button press."""
        print("Login")
        print(f"Username: {self.login_subframe.login_username_box.get().strip()}")
        print(f"Tag: {self.login_subframe.login_tag_box.get().strip()}")
        print(f"Password: {self.login_subframe.login_password_box.get().strip()}")

    def on_register(self, event: Event) -> None:
        """On login button press."""
        print("Register")
        print(f"Username: {self.register_subframe.register_username_box.get().strip()}")
        print(f"Password: {self.register_subframe.register_password_box.get().strip()}")


class TestFrame(tkb.Frame):
    """Frame for testing and creating."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Test")
        pass
