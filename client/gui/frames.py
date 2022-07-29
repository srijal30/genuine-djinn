import asyncio
import tkinter as tk
from tkinter import Event
from typing import Any, Dict

import ttkbootstrap as tkb  # type: ignore
from ttkbootstrap.scrolled import ScrolledText

__app__ = (
    "ChatFrame",
    "ConnectionFrame",
    "LoginFrame",
    "RegisterFrame",
    "TestFrame"
)


class ChatFrame(tkb.Frame):
    """Frame for chat page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Chat")

        self.grid(
            row=0, rowspan=3,
            column=0, columnspan=3,
            padx=3, pady=3,
            sticky=tkb.NSEW
        )

        self.menu_subframe = self.MenuSubframe(self, self.master)
        self.chat_subframe = self.ChatSubframe(self, self.master)
        self.entry_subframe = self.EntrySubframe(self, self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    class Message(tkb.Label):
        """Message class."""

        def __init__(self, container, msg: Dict[str, Any]):
            tkb.Label.__init__(self, container)

            self.msg_data = msg

            self.container = container
            self.msg = f"{self.msg_data['author']['name']}: {self.msg_data['content']}"
            self.setup()

        def setup(self) -> None:
            """Configure the Label object."""
            self.config(
                text=self.msg,
                justify="left",
                wraplength=self.master.winfo_width() * 0.75,
            )

        def set_msg(self, msg: Dict[str, Any]) -> None:
            """Updates the message object."""
            self.msg_data = msg
            self.msg = f"{self.msg_data['author']['name']}: {self.msg_data['content']}"
            self.setup()

    class MenuSubframe(tkb.Frame):
        """Subframe for chat menu."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(
                row=0, rowspan=1,
                column=0, columnspan=3,
                sticky=tkb.NSEW
            )
            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            self.room_info = tkb.Label(self)
            self.room_info.configure(text="Room Info")
            self.room_info.grid(
                row=0,
                column=0,
                padx=2,
                sticky=tkb.NSEW
            )

            self.menu_btn = tkb.Button(self)
            self.menu_btn.configure(text="Menu")
            self.menu_btn.grid(
                row=0,
                column=1,
                padx=2,
                sticky=tkb.NSEW
            )
            self.menu_btn.bind("<ButtonPress>", self.parent.on_menu)

            self.leave_btn = tkb.Button(self)
            self.leave_btn.configure(text="Leave")
            self.leave_btn.grid(
                row=0,
                column=2,
                padx=2,
                sticky=tkb.NSEW
            )
            self.leave_btn.bind("<ButtonPress>", self.parent.on_leave)

    class ChatSubframe(tkb.Frame):
        """Subframe for scrolling chat."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(
                row=1, rowspan=1,
                column=0, columnspan=3,
                sticky=tkb.NSEW
            )
            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            self.chat_box = ScrolledText(self, bootstyle="round")
            self.chat_box.text.configure(state="disable")
            self.chat_box.grid(
                row=1, rowspan=1,
                column=0, columnspan=3,
                sticky=tkb.NSEW
            )

    class EntrySubframe(tkb.Frame):
        """Subframe for chat entry and sending."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(
                row=2, rowspan=1,
                column=0, columnspan=3,
                sticky=tkb.NSEW
            )
            self.columnconfigure(0, weight=1)

            self.message_box = tkb.Entry(self, bootstyle="secondary")
            self.message_box.configure(textvariable=tk.StringVar(value=""))
            self.message_box.grid(
                row=2,
                column=0,
                padx=2,
                sticky=tkb.NSEW
            )
            self.message_box.bind("<Return>", self.parent.on_send)

            self.char_btn = tkb.Button(self)
            self.char_btn.configure(text="Emotes")
            self.char_btn.grid(
                row=2,
                column=1,
                padx=2,
                sticky=tkb.NSEW
            )
            self.char_btn.bind("<ButtonPress>", self.parent.on_char)

            self.send_btn = tkb.Button(self)
            self.send_btn.configure(text="Send")
            self.send_btn.grid(
                row=2,
                column=2,
                padx=2,
                sticky=tkb.NSEW
            )
            self.send_btn.bind("<ButtonPress>", self.parent.on_send)

    def on_send(self, event: Event) -> None:
        """On send button or enter press. Send message."""
        msg = self.entry_subframe.message_box.get().strip()

        if len(msg) > 0:
            print(f"Message: {msg}")
            self.master.send_message(msg)
            self.entry_subframe.message_box.delete(0, "end")

    def on_menu(self, event: Event) -> None:
        """Open chat option menu when button pressed."""
        self.last_msg.set_msg("Potato")
        print("chat menu")

    def on_leave(self, event: Event) -> None:
        """On leave button being pressed. Leave chat room."""
        # stop the connection
        loop = self.master.loop
        task = loop.create_task(self.master.connection.exit_room())

        def callback(result: asyncio.Task) -> None:
            success = result.result()
            print(f"leaving room was success:{success}")

        task.add_done_callback(callback)
        # add code to stop receiving messages if requiered

    def on_char(self, event: Event) -> None:
        """Open char menu on button click."""
        print("emote/character menu")

    def set_info(self, message: str) -> None:
        """Set message at top of chat room."""
        self.menu_subframe.room_info.configure(text=message)

    def display_message(self, message: Dict[str, Any]) -> None:
        """Displays message in chat."""
        self.chat_subframe.chat_box.text.configure(state="normal")

        self.msg = self.Message(self.chat_subframe.chat_box, message)

        self.chat_subframe.chat_box.insert("end", "\n")
        self.chat_subframe.chat_box.window_create("end", window=self.msg, pady=2)
        self.chat_subframe.chat_box.text.configure(state="disable")
        self.chat_subframe.chat_box.text.yview_moveto(1)

    def clear_chat(self) -> None:
        """Clears contents of the ScrolledText chat."""
        self.chat_subframe.chat_box.text.configure(state="normal")
        self.chat_subframe.chat_box.text.delete("1.0", "end")
        self.chat_subframe.chat_box.text.configure(state="disable")


class ConnectFrame(tkb.Frame):
    """Frame for connect page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Connect")

        self.grid_anchor("center")
        self.grid(
            row=0, rowspan=3,
            column=0, columnspan=3,
            padx=3, pady=3,
            sticky=tkb.NSEW
        )

        self.join_subframe = self.JoinSubframe(self, self.master)
        self.create_subframe = self.CreateSubframe(self, self.master)
        self.connect_subframe = self.ConnectSubframe(self, self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    class JoinSubframe(tkb.Frame):
        """Subframe for joining a room."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(
                row=0, rowspan=3,
                column=0, columnspan=1
            )

            self.join_label = tkb.Label(self)
            self.join_label.configure(text="Join Room")
            self.join_label.grid(
                row=0,
                column=0
            )

            self.join_box = tkb.Entry(self)
            self.join_box.grid(
                row=1,
                column=0,
                padx=20, pady=5
            )
            self.join_box.bind("<Return>", self.parent.on_join)

            self.join_btn = tkb.Button(self)
            self.join_btn.configure(text="Join")
            self.join_btn.grid(
                row=2,
                column=0,
                pady=3
            )
            self.join_btn.bind("<ButtonPress>", self.parent.on_join)

    class CreateSubframe(tkb.Frame):
        """Subframe for creating a room."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(
                row=0, rowspan=3,
                column=1, columnspan=1
            )

            self.create_label = tkb.Label(self)
            self.create_label.configure(text="Make Room")
            self.create_label.grid(
                row=0,
                column=1
            )

            self.create_box = tkb.Entry(self)
            self.create_box.grid(
                row=1,
                column=1,
                padx=20, pady=5
            )
            self.create_box.bind("<Return>", self.parent.on_create)

            self.room_btn = tkb.Button(self)
            self.room_btn.configure(text="Create")
            self.room_btn.grid(
                row=2,
                column=1,
                pady=3
            )
            self.room_btn.bind("<ButtonPress>", self.parent.on_create)

    class ConnectSubframe(tkb.Frame):
        """Subframe for connecting to a room."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid(
                row=0, rowspan=3,
                column=2, columnspan=1
            )

            self.connect_label = tkb.Label(self)
            self.connect_label.configure(text="Connect to Room")
            self.connect_label.grid(
                row=0,
                column=2
            )

            self.connect_box = tkb.Entry(self)
            self.connect_box.grid(
                row=1,
                column=2,
                padx=20, pady=5
            )
            self.connect_box.bind("<Return>", self.parent.on_connect)

            self.connect_btn = tkb.Button(self)
            self.connect_btn.configure(text="Connect")
            self.connect_btn.grid(
                row=2,
                column=2,
                pady=3
            )
            self.connect_btn.bind("<ButtonPress>", self.parent.on_connect)

    # you have to enter name here not code
    def on_create(self, event: Event) -> None:
        """On Create Room button press."""
        new_name = str(self.create_subframe.create_box.get().strip())

        loop = self.master.loop
        task = loop.create_task(self.master.connection.create_room(new_name))

        def callback(result: asyncio.Task) -> None:
            room_info = result.result()
            print(f"New room code is: {room_info[0]}")
            print(f"New room id is: {room_info[1]}")

        task.add_done_callback(callback)

    def on_join(self, event: Event) -> None:
        """On Join Room button press."""
        code = str(self.join_subframe.join_box.get().strip())

        loop = self.master.loop
        task = loop.create_task(self.master.connection.join_room(code))

        def callback(result: asyncio.Task) -> None:
            print(f"ID of the newly joined room is: {id}")

        task.add_done_callback(callback)

    def on_connect(self, event: Event) -> None:
        """On Connect button being pressed."""
        id = int(self.connect_subframe.connect_box.get())
        # connect to the room

        loop = self.master.loop
        task = loop.create_task(self.master.connection.connect_room(id))

        def callback(result: asyncio.Task) -> None:
            success = result.result()
            print(f"connecting to room was a success: {success}")
            if success:
                # start receiving messages and open chatroom
                receive_task = self.master.connection.receive_messages(
                    self.master.receive_message
                )
                loop.create_task(receive_task)
                self.master.switch_frame(ChatFrame)

        task.add_done_callback(callback)


class LoginFrame(tkb.Frame):
    """Frame for login page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Login")

        self.grid_anchor("center")
        self.grid(
            row=0, rowspan=5,
            column=0, columnspan=2,
            sticky=tkb.NSEW
        )

        self.header_subframe = self.HeaderSubframe(self, self.master)
        self.login_subframe = self.LoginSubframe(self, self.master)
        self.info_subframe = self.InfoSubframe(self, self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    class HeaderSubframe(tkb.Frame):
        """Subframe for header information."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid_anchor("center")
            self.grid(
                row=0, rowspan=2,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )

            self.name_label = tkb.Label(self, font=("MS Sans Serif", 50))
            self.name_label.configure(text="Glitchat")
            self.name_label.grid(
                row=0, rowspan=1,
                column=0, columnspan=2,
                pady=20,
                sticky=tkb.NSEW
            )

            self.form_label = tkb.Label(self, font=("Sans Serif Bold", 20))
            self.form_label.configure(text="Login", justify="center")
            self.form_label.grid(
                row=1, rowspan=1,
                column=0, columnspan=2,
                pady=20,
                sticky=tkb.NS
            )

    class LoginSubframe(tkb.Frame):
        """Subframe for login form."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid_anchor("center")
            self.grid(
                row=2, rowspan=4,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )

            self.login_username_box = tkb.Entry(self, font=("Sans Serif", 14))
            self.login_username_box.insert("end", "username...")
            self.login_username_box.grid(
                row=2, rowspan=1,
                column=0, columnspan=2,
                padx=5, pady=3,
                ipadx=10, ipady=5
            )
            self.login_username_box.bind("<Return>", self.parent.on_login)

            self.login_tag_box = tkb.Entry(self, font=("Sans Serif", 14))
            self.login_tag_box.insert("end", "tag...")
            self.login_tag_box.grid(
                row=3, rowspan=1,
                column=0, columnspan=2,
                padx=5, pady=3,
                ipadx=10, ipady=5
            )
            self.login_tag_box.bind("<Return>", self.parent.on_login)

            self.login_password_box = tkb.Entry(self, font=("Sans Serif", 14))  # show="*"
            self.login_password_box.insert("end", "password...")
            self.login_password_box.grid(
                row=4, rowspan=1,
                column=0, columnspan=2,
                padx=5, pady=3,
                ipadx=10, ipady=5
            )
            self.login_password_box.bind("<Return>", self.parent.on_login)

            self.login_btn_style = tkb.Style()
            self.login_btn_style.configure("login.TButton", font=("Sans Serif", 16))
            self.login_btn = tkb.Button(self)
            self.login_btn.configure(text="Submit", style="login.TButton")
            self.login_btn.grid(
                row=5, rowspan=1,
                column=0, columnspan=2,
                padx=30, pady=15,
                ipady=2,
                sticky=tkb.NSEW
            )
            self.login_btn.bind("<ButtonPress>", self.parent.on_login)

    class InfoSubframe(tkb.Frame):
        """Subframe for login/registration info."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid_anchor("center")
            self.grid(
                row=6, rowspan=1,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )

            self.info_label = tkb.Label(self, font=("Sans Serif", 10))
            self.info_label.configure(text="Don't have an account?  ")
            self.info_label.grid(
                row=6, rowspan=1,
                column=0, columnspan=1
            )

            self.login_btn_style = tkb.Style()
            self.login_btn_style.configure("register.TButton", font=("Sans Serif", 10))
            self.register_btn = tkb.Button(self)
            self.register_btn.configure(text="Register", style="register.TButton")
            self.register_btn.grid(
                row=6, rowspan=1,
                column=1, columnspan=1,
                pady=30,
                sticky=tkb.NSEW
            )
            self.register_btn.bind("<ButtonPress>", self.parent.switch_register)

    def on_login(self, event: Event) -> None:
        """On login button press."""
        print("Login")
        print(f"Username: {self.login_subframe.login_username_box.get().strip()}")
        print(f"Tag: {self.login_subframe.login_tag_box.get().strip()}")
        print(f"Password: {self.login_subframe.login_password_box.get().strip()}")

    def switch_register(self, event: Event) -> None:
        """Switch to register frame."""
        self.master.switch_frame(RegisterFrame)


class RegisterFrame(tkb.Frame):
    """Frame for registration page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Register")

        self.grid_anchor("center")
        self.grid(
            row=0, rowspan=5,
            column=0, columnspan=2,
            sticky=tkb.NSEW
        )

        self.header_subframe = self.HeaderSubframe(self, self.master)
        self.register_subframe = self.RegisterSubframe(self, self.master)
        self.info_subframe = self.InfoSubframe(self, self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    class HeaderSubframe(tkb.Frame):
        """Subframe for header information."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid_anchor("center")
            self.grid(
                row=0, rowspan=2,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )

            self.name_label = tkb.Label(self, font=("MS Sans Serif", 50))
            self.name_label.configure(text="Glitchat")
            self.name_label.grid(
                row=0, rowspan=1,
                column=0, columnspan=2,
                pady=20, sticky=tkb.NSEW
            )

            self.form_label = tkb.Label(self, font=("Sans Serif Bold", 20))
            self.form_label.configure(text="Register", justify="center")
            self.form_label.grid(
                row=1, rowspan=1,
                column=0, columnspan=2,
                pady=20,
                sticky=tkb.NS
            )

    class RegisterSubframe(tkb.Frame):
        """Subframe for registration form."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid_anchor("center")
            self.grid(row=2, rowspan=2, column=0, columnspan=2, sticky=tkb.NSEW)

            self.register_username_box = tkb.Entry(self, font=("Sans Serif", 14))
            self.register_username_box.insert("end", "username...")
            self.register_username_box.grid(
                row=2, rowspan=1,
                column=0, columnspan=2,
                padx=5, pady=3,
                ipadx=10, ipady=5
            )
            self.register_username_box.bind("<Return>", self.parent.on_register)

            self.register_password_box = tkb.Entry(self, font=("Sans Serif", 14))  # show="*"
            self.register_password_box.insert("end", "password...")
            self.register_password_box.grid(
                row=3, rowspan=1,
                column=0, columnspan=2,
                padx=5, pady=3,
                ipadx=10, ipady=5
            )
            self.register_password_box.bind("<Return>", self.parent.on_register)

            self.register_btn_style = tkb.Style()
            self.register_btn_style.configure("register.TButton", font=("Sans Serif", 16))
            self.register_btn = tkb.Button(self)
            self.register_btn.configure(text="Submit", style="register.TButton")
            self.register_btn.grid(
                row=4, rowspan=1,
                column=0, columnspan=2,
                padx=30, pady=15,
                ipady=2,
                sticky=tkb.NSEW
            )
            self.register_btn.bind("<ButtonPress>", self.parent.on_register)

    class InfoSubframe(tkb.Frame):
        """Subframe for login/registration info."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent = parent
            self.master = master

            self.grid_anchor("center")
            self.grid(
                row=4, rowspan=1,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )

            self.info_label = tkb.Label(self, font=("Sans Serif", 10))
            self.info_label.configure(text="Already have an account?  ")
            self.info_label.grid(
                row=5, rowspan=1,
                column=0, columnspan=1
            )

            self.login_btn_style = tkb.Style()
            self.login_btn_style.configure("login.TButton", font=("Sans Serif", 10))
            self.login_btn = tkb.Button(self)
            self.login_btn.configure(text="Login", style="login.TButton")
            self.login_btn.grid(
                row=5, rowspan=1,
                column=1, columnspan=1,
                pady=30,
                sticky=tkb.NSEW
            )
            self.login_btn.bind("<ButtonPress>", self.parent.switch_login)

    def on_register(self, event: Event) -> None:
        """On registration button press."""
        username = self.register_subframe.register_username_box.get().strip()
        password = self.register_subframe.register_password_box.get().strip()

        loop = self.master.loop
        task = loop.create_task(self.master.connection.register(username, password))

        def callback(result: asyncio.Task) -> None:
            tag = result.result()
            print(f"your tag is {tag}")

        task.add_done_callback(callback)

    def switch_login(self, event: Event) -> None:
        """Switch to login frame."""
        self.master.switch_frame(LoginFrame)


class TestFrame(tkb.Frame):
    """Frame for testing stuff."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Test")
