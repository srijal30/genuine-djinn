from __future__ import annotations

import asyncio
import tkinter as tk
from tkinter import Event
from typing import TYPE_CHECKING, Any, Dict

import ttkbootstrap as tkb  # type: ignore
from components import Message
from ttkbootstrap.scrolled import ScrolledText

if TYPE_CHECKING:
    from app import ChatApp


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

        self.master: ChatApp = master

        self.master.title("Glitchat - Chat")

        self.grid(
            row=0, rowspan=3,
            column=0, columnspan=3,
            padx=3, pady=3,
            sticky=tkb.NSEW
        )

        self.menu_subframe = self.MenuSubframe(self, self.master)
        self.chat_subframe = self.ChatSubframe(self, self.master)
        self.entry_subframe = self.EntrySubframe(self, self.master)
        self.sidebar_subframe = self.SidebarSubframe(self, self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    class MenuSubframe(tkb.Frame):
        """Subframe for chat menu."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent: ChatFrame = parent
            self.master: ChatApp = master

            self.grid(
                row=0, rowspan=1,
                column=0, columnspan=1,
                sticky=tkb.NSEW
            )
            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            self.cr: Dict[str, Any] = self.master.current_room

            self.room_info = tkb.Label(self, font=("Sans Serif Bold", 12))
            self.room_info.configure(
                text=f"{self.cr['name']}   |   Invite Code: {self.cr['code']}   |   ID: {self.cr['id']}"
            )
            self.room_info.grid(
                row=0,
                column=0,
                padx=2,
                sticky=tkb.NSEW
            )

    class ChatSubframe(tkb.Frame):
        """Subframe for scrolling chat."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent: ChatFrame = parent
            self.master: ChatApp = master

            self.grid(
                row=1, rowspan=1,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )
            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            self.chat_box = ScrolledText(self, bootstyle="round")
            self.chat_box.text.configure(state="disable")
            self.chat_box.grid(
                row=1, rowspan=1,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )

    class EntrySubframe(tkb.Frame):
        """Subframe for chat entry and sending."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent: ChatFrame = parent
            self.master: ChatApp = master

            self.grid(
                row=2, rowspan=1,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )
            self.columnconfigure(0, weight=1)

            self.message_box = tkb.Entry(self, bootstyle="secondary", font=("Sans Serif", 12))
            self.message_box.configure(textvariable=tk.StringVar(value=""))
            self.message_box.grid(
                row=2,
                column=0,
                padx=2,
                sticky=tkb.NSEW
            )
            self.message_box.bind("<Return>", self.parent.on_send)

            self.login_btn_style = tkb.Style()
            self.login_btn_style.configure("send.TButton", font=("Sans Serif Bold", 16))
            self.send_btn = tkb.Button(self)
            self.send_btn.configure(text=">", style="send.TButton")
            self.send_btn.grid(
                row=2,
                column=1,
                padx=2,
                sticky=tkb.NSEW
            )
            self.send_btn.bind("<ButtonPress>", self.parent.on_send)

    class SidebarSubframe(tkb.Frame):
        """Subframe for sidebar containing chat room information."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent: ChatFrame = parent
            self.master: ChatApp = master

            self.grid(
                row=0, rowspan=4,
                column=2, columnspan=1,
                sticky=tkb.NSEW
            )
            self.columnconfigure(0, weight=1)

            self.room_info = tkb.Label(self, font=("Sans Serif Bold", 14))
            self.room_info.configure(text="Users:")
            self.room_info.grid(
                row=0,
                column=2,
                padx=2,
                sticky=tkb.NS
            )

            self.user_label = tkb.Text(self, width=25)
            self.user_label.grid(
                row=1, rowspan=2,
                column=2, columnspan=1,
                padx=2,
                sticky=tkb.NSEW
            )

            self.user_label.configure(state="normal")

            for user in self.master.current_room["users"]:
                self.user_label.insert("end", f"{user['name']}#{user['tag']}\n")

            self.user_label.configure(state="disable")

    def on_send(self, event: Event) -> None:
        """On send button or enter press. Send message."""
        msg = self.entry_subframe.message_box.get().strip()

        if len(msg) > 0:
            print(f"Message: {msg}")
            self.master.send_message(msg)
            self.entry_subframe.message_box.delete(0, "end")

    def on_leave(self, event: Event) -> None:
        """On leave button being pressed. Leave chat room."""
        # disconnect from chatroom request
        loop = self.master.loop
        task = loop.create_task(self.master.connection.exit_room())

        def callback(result: asyncio.Task) -> None:
            success = result.result()
            print(f"leaving room was success:{success}")  # DEBUG

        task.add_done_callback(callback)
        # add code to stop receiving messages if required

    def display_message(self, message: Dict[str, Any]) -> None:
        """Displays message in chat."""
        self.chat_subframe.chat_box.text.configure(state="normal")

        self.msg = Message(self.chat_subframe.chat_box, self.master, message)

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

        self.master.title("Glitchat - Connect")

        self.grid_anchor("center")
        self.grid(
            row=0, rowspan=20,
            column=0, columnspan=3,
            padx=3, pady=3,
            sticky=tkb.NSEW
        )

        self.header_subframe = self.HeaderSubframe(self, self.master)
        self.join_subframe = self.JoinSubframe(self, self.master)
        self.create_subframe = self.CreateSubframe(self, self.master)
        self.room_subframe = None
        self.update_rooms()

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    def update_rooms(self) -> None:
        """Update room subframe."""
        loop = self.master.loop
        task = loop.create_task(self.master.get_room_list())

        def callback(result: asyncio.Task):
            self.room_subframe = self.RoomSubframe(self, self.master)

        task.add_done_callback(callback)

    class HeaderSubframe(tkb.Frame):
        """Subframe for header information (username, tag, etc.)."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent: ConnectFrame = parent
            self.master: ChatApp = master

            self.grid_anchor("center")
            self.grid(
                row=0, rowspan=2,
                column=0, columnspan=3,
                pady=30
            )

            self.login_as_label = tkb.Label(self, font=("Sans Serif Bold", 16))
            self.login_as_label.configure(text="Logged in as: ")
            self.login_as_label.grid(
                row=0, rowspan=2,
                column=0, columnspan=1,
                padx=10, pady=0,
                sticky=tkb.NSEW
            )

            self.username_label = tkb.Label(self, font=("Sans Serif", 13))
            self.username_label.configure(text=f"{self.master.user}#{self.master.tag}")
            self.username_label.grid(
                row=0, rowspan=2,
                column=1, columnspan=2,
                padx=5, pady=0,
                sticky=tkb.NSEW
            )

    class JoinSubframe(tkb.Frame):
        """Subframe for joining a room."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent: ConnectFrame = parent
            self.master: ChatApp = master

            self.grid_anchor("center")
            self.grid(
                row=2, rowspan=3,
                column=0, columnspan=1,
                pady=5
            )

            self.join_label = tkb.Label(self, font=("Sans Serif", 12))
            self.join_label.configure(text="Join Room")
            self.join_label.grid(
                row=2,
                column=0,
                pady=2
            )

            self.join_box = tkb.Entry(self, font=("Sans Serif", 14), justify="center")
            self.join_box.grid(
                row=3,
                column=0,
                padx=10, pady=2
            )
            self.join_box.bind("<Return>", self.parent.on_join)

            self.register_btn_style = tkb.Style()
            self.register_btn_style.configure("join.TButton", font=("Sans Serif", 14))
            self.join_btn = tkb.Button(self)
            self.join_btn.configure(text="Submit", style="join.TButton")
            self.join_btn.grid(
                row=4,
                column=0,
                pady=2
            )
            self.join_btn.bind("<ButtonPress>", self.parent.on_join)

    class CreateSubframe(tkb.Frame):
        """Subframe for creating a room."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent: ConnectFrame = parent
            self.master: ChatApp = master

            self.grid_anchor("center")
            self.grid(
                row=2, rowspan=3,
                column=2, columnspan=1,
                pady=5
            )

            self.create_label = tkb.Label(self, font=("Sans Serif", 12))
            self.create_label.configure(text="Create Room")
            self.create_label.grid(
                row=2,
                column=2,
                pady=2
            )

            self.create_box = tkb.Entry(self, font=("Sans Serif", 14), justify="center")
            self.create_box.grid(
                row=3,
                column=2,
                padx=10, pady=2
            )
            self.create_box.bind("<Return>", self.parent.on_create)

            self.register_btn_style = tkb.Style()
            self.register_btn_style.configure("create.TButton", font=("Sans Serif", 14))
            self.room_btn = tkb.Button(self)
            self.room_btn.configure(text="Submit", style="create.TButton")
            self.room_btn.grid(
                row=4,
                column=2,
                pady=2
            )
            self.room_btn.bind("<ButtonPress>", self.parent.on_create)

    class RoomSubframe(tkb.Frame):
        """Subframe for managing rooms."""

        def __init__(self, parent, master):
            tkb.Frame.__init__(self, parent)

            self.parent: ConnectFrame = parent
            self.master: ChatApp = master

            self.grid_anchor("center")
            self.grid(
                row=5, rowspan=10,
                column=0, columnspan=3
            )

            self.room_label = tkb.Label(self, font=("Sans Serif Bold", 14))
            self.room_label.configure(
                text="Your Rooms:"
            )
            self.room_label.grid(
                row=4, rowspan=1,
                column=1, columnspan=1,
                padx=5, pady=20,
                sticky=tkb.NSEW
            )

            # local variables for generating room grid
            self.row = 6
            self.col = 0

            for rm in self.master.room_list:
                self.add_room(rm)

        def add_room(self, room: Dict[str, Any]) -> None:
            """Add a room to the room grid."""
            self.room_box = tkb.Label(self, font=("Sans Serif", 12))
            self.room_box.configure(
                text=f"  {room['name']}#{room['id']}",
                justify="center"
            )
            self.room_box.grid(
                row=self.row, rowspan=1,
                column=self.col, columnspan=1,
                padx=10, pady=10,
                ipadx=1, ipady=5,
                sticky=tkb.NSEW
            )
            self.room_box.bind("<Button-1>", lambda e: self.parent.on_connect(room["id"]))

            self.col += 1

            if self.col == 3:
                self.col = 0
                self.row += 1

    def on_create(self, event: Event) -> None:
        """On Create Room button press."""
        new_name = self.create_subframe.create_box.get().strip()

        # error handling
        if not new_name:
            self.master.popup('error', 'Please fill out all the required fields!')
            return

        loop = self.master.loop
        task = loop.create_task(self.master.connection.create_room(new_name))

        # POPUP
        def callback(result: asyncio.Task) -> None:
            room_info = result.result()
            self.update_rooms()

            self.master.popup(
                type='success',
                message=f'Creation of the room was a success\n \
                Your room code: {room_info[0]}\nYour room id: {room_info[1]}'
            )
            print(f"New room code is: {room_info[0]}")
            print(f"New room id is: {room_info[1]}")

        task.add_done_callback(callback)

    def on_join(self, event: Event) -> None:
        """On Join Room button press."""
        code = str(self.join_subframe.join_box.get().strip())

        loop = self.master.loop
        task = loop.create_task(self.master.connection.join_room(code))

        def callback(result: asyncio.Task) -> None:
            # check if there was an error joining the room
            try:
                name = result.result()['name']
                self.update_rooms()
                self.master.popup('success', f'You have successfully joined with name "{name}"')
            except Exception:
                self.master.popup('error', "An error occured when trying to join the room\n \
                Make sure that you haven't already joined the room")

        task.add_done_callback(callback)

    def on_connect(self, id: int) -> None:
        """On Connect button being pressed."""
        # connect to the room
        loop = self.master.loop
        task = loop.create_task(self.master.connection.connect_room(id))

        for rm in self.master.room_list:
            if rm["id"] == id:
                self.master.current_room = rm
            break

        def callback(result: asyncio.Task) -> None:
            success = result.result()
            print(f"connecting to room was a success: {success}")
            if success:
                # start receiving messages and open chatroom
                receive_task = self.master.connection.message_listener(
                    self.master.receive_message
                )
                loop.create_task(receive_task)
                self.master.switch_frame(ChatFrame)

        task.add_done_callback(callback)


class LoginFrame(tkb.Frame):
    """Frame for login page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master: ChatApp = master

        self.master.title("Glitchat - Login")

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

            self.parent: LoginFrame = parent
            self.master: ChatApp = master

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

            self.parent: LoginFrame = parent
            self.master: ChatApp = master

            self.grid_anchor("center")
            self.grid(
                row=2, rowspan=4,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )

            self.login_username_label = tkb.Label(self, font=("Sans Serif", 14))
            self.login_username_label.configure(text="Username", justify="right")
            self.login_username_label.grid(
                row=2, rowspan=1,
                column=0, columnspan=1,
                pady=20,
                sticky=tkb.E
            )

            self.login_username_box = tkb.Entry(self, font=("Sans Serif", 14))
            self.login_username_box.grid(
                row=2, rowspan=1,
                column=1, columnspan=1,
                padx=5, pady=3,
                ipadx=10, ipady=5
            )
            self.login_username_box.bind("<Return>", self.parent.on_login)

            self.login_tag_label = tkb.Label(self, font=("Sans Serif", 14))
            self.login_tag_label.configure(text="Tag", justify="right")
            self.login_tag_label.grid(
                row=3, rowspan=1,
                column=0, columnspan=1,
                pady=20,
                sticky=tkb.E
            )

            self.login_tag_box = tkb.Entry(self, font=("Sans Serif", 14))
            self.login_tag_box.grid(
                row=3, rowspan=1,
                column=1, columnspan=1,
                padx=5, pady=3,
                ipadx=10, ipady=5
            )
            self.login_tag_box.bind("<Return>", self.parent.on_login)

            self.login_password_label = tkb.Label(self, font=("Sans Serif", 14))
            self.login_password_label.configure(text="Password", justify="right")
            self.login_password_label.grid(
                row=4, rowspan=1,
                column=0, columnspan=1,
                pady=20,
                sticky=tkb.E
            )

            self.login_password_box = tkb.Entry(self, font=("Sans Serif", 14), show="*")
            self.login_password_box.grid(
                row=4, rowspan=1,
                column=1, columnspan=1,
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

            self.parent: LoginFrame = parent
            self.master: ChatApp = master

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
        self.master.user = username = self.login_subframe.login_username_box.get().strip()
        tag = self.login_subframe.login_tag_box.get().strip()
        password = self.login_subframe.login_password_box.get().strip()

        # Make sure all the fields are filled out
        if not password or not tag or not username:
            self.master.popup('error', 'Please fill out all the required fields!')
            return
        # Make sure that tag is a numeric value
        try:
            self.master.tag = tag = int(tag)
        except Exception:
            self.master.popup('error', 'Tag is supposed to be a numeric value!')
            return

        loop = self.master.loop
        task = loop.create_task(self.master.connection.login(username, tag, password))

        # POPUP
        def callback(result: asyncio.Task) -> None:
            success = result.result()
            if success:
                self.master.switch_frame(ConnectFrame)
                self.master.popup('success', 'You are logged in!')
            else:
                self.master.popup('error', 'Login was unsucessful')

        task.add_done_callback(callback)

    def switch_register(self, event: Event) -> None:
        """Switch to register frame."""
        self.master.switch_frame(RegisterFrame)


class RegisterFrame(tkb.Frame):
    """Frame for registration page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master: ChatApp = master

        self.master.title("Glitchat - Register")

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

            self.parent: RegisterFrame = parent
            self.master: ChatApp = master

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

            self.parent: RegisterFrame = parent
            self.master: ChatApp = master

            self.grid_anchor("center")
            self.grid(
                row=2, rowspan=2,
                column=0, columnspan=2,
                sticky=tkb.NSEW
            )

            self.register_username_label = tkb.Label(self, font=("Sans Serif", 14))
            self.register_username_label.configure(text="Username", justify="right")
            self.register_username_label.grid(
                row=2, rowspan=1,
                column=0, columnspan=1,
                pady=20,
                sticky=tkb.E
            )

            self.register_username_box = tkb.Entry(self, font=("Sans Serif", 14))
            self.register_username_box.grid(
                row=2, rowspan=1,
                column=1, columnspan=1,
                padx=5, pady=3,
                ipadx=10, ipady=5
            )
            self.register_username_box.bind("<Return>", self.parent.on_register)

            self.register_password_label = tkb.Label(self, font=("Sans Serif", 14))
            self.register_password_label.configure(text="Password", justify="right")
            self.register_password_label.grid(
                row=3, rowspan=1,
                column=0, columnspan=1,
                pady=20,
                sticky=tkb.E
            )

            self.register_password_box = tkb.Entry(self, font=("Sans Serif", 14), show="*")
            self.register_password_box.grid(
                row=3, rowspan=1,
                column=1, columnspan=1,
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

            self.parent: RegisterFrame = parent
            self.master: ChatApp = master

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
        self.master.user = username = self.register_subframe.register_username_box.get().strip()
        password = self.register_subframe.register_password_box.get().strip()

        # Make sure all the fields are filled out
        if not password or not username:
            self.master.popup('error', 'Please fill out all the required fields!')
            return

        loop = self.master.loop
        task = loop.create_task(self.master.connection.register(username, password))

        def callback(result: asyncio.Task) -> None:
            self.master.tag = tag = result.result()
            self.master.popup('success', f'Your generated tag is {tag}')
            self.master.switch_frame(ConnectFrame)

        task.add_done_callback(callback)

    def switch_login(self, event: Event) -> None:
        """Switch to login frame."""
        self.master.switch_frame(LoginFrame)


class TestFrame(tkb.Frame):
    """Frame for testing stuff."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master: ChatApp = master

        self.master.title("Glitchat - Test")
