import asyncio
# import threading  # using this for a temp solution

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

        self.leave_btn = tkb.Button(self.message_frame)
        self.leave_btn.configure(text="Leave")
        self.leave_btn.bind("<ButtonPress>", self.on_leave)
        self.leave_btn.grid(row=0, column=3, padx=2)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

    def on_send(self, event: Event) -> None:
        """On send button or enter press. Send message."""
        msg = self.message_box.get().strip()

        if len(msg) > 0:
            print(f"Message: {msg}")
            self.master.send_message(msg)
            self.message_box.delete(0, "end")

    def on_leave(self, event: Event) -> None:
        """On leave button being pressed. Leave chat room."""
        print("Leave")

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

        self.master = master

        self.master.title("Chat App - Connect")

        self.create_label = ttk.Label(self)
        self.create_label.configure(text="Make Room")
        self.create_label.grid(column=0, row=0)

        self.create_box = ttk.Entry(self)
        self.create_box.grid(column=0, padx=20, pady=5, row=1, sticky="w")
        self.create_box.bind("<Return>", self.on_create)

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

        self.connect_label = ttk.Label(self)
        self.connect_label.configure(text="Connect to Room")
        self.connect_label.grid(column=4, row=0)

        self.connect_box = ttk.Entry(self)
        self.connect_box.grid(column=4, padx=20, pady=5, row=1)
        self.connect_box.bind("<Return>", self.on_connect)

        self.connect_btn = ttk.Button(self)
        self.connect_btn.configure(text="Connect")
        self.connect_btn.bind("<ButtonPress>", self.on_connect)
        self.connect_btn.grid(column=4, pady=3, row=2)

        self.grid_anchor("center")
        self.grid(column=0, columnspan=5, row=0, rowspan=3, sticky=tk.NSEW)

    # you have to enter name here not code
    def on_create(self, event: Event) -> None:
        """On Create Room button press."""
        # print(f"Room Name (Create): {self.create_box.get().strip()}")
        new_name = self.create_box.get().strip()

        loop = asyncio.get_event_loop()
        room_info = loop.run_until_complete(self.master.connection.create_room(new_name))
        # room_info = await self.master.connection.create_room(new_name)
        print(f"New room code is: {room_info[0]}")
        print(f"New room id is: {room_info[1]}")

    def on_join(self, event: Event) -> None:
        """On Join Room button press."""
        # print(f"Room Code (Join): {self.join_box.get().strip()}")
        code = self.join_box.get().strip()

        loop = asyncio.get_event_loop()
        id = loop.run_until_complete(self.master.connection.join_room(code))
        # id = await self.master.connection.join_room(code)
        print(f"ID of the newly joined room is: {id}")

    def on_connect(self, event: Event) -> None:
        """On Connect button being pressed."""
        id = int(self.connect_box.get())
        # connect to the room
        loop = asyncio.get_event_loop()
        success = loop.run_until_complete(self.master.connection.connect_room(id))
        print(success)

        # switch frame
        self.master.switch_frame(ChatFrame)
        # add this to a thread
        # receive_message_task = self.master.connection.receive_messages(self.master.receive_message)
        # _thread = threading.Thread(target=asyncio.run, args=receive_message_task)


class LoginFrame(tkb.Frame):
    """Frame for login page."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Login")

        # login
        self.login_username_label = tkb.Label(self)
        self.login_username_label.configure(text="Username")
        self.login_username_label.grid(column=0, padx=5, row=0, sticky="e")

        self.login_username_box = tkb.Entry(self)
        self.login_username_box.grid(column=1, ipadx=10, pady=3, row=0, sticky="w")
        self.login_username_box.bind("<Return>", self.on_login)

        self.login_tag_label = tkb.Label(self)
        self.login_tag_label.configure(text="Tag")
        self.login_tag_label.grid(column=0, padx=5, row=1, sticky="e")

        self.login_tag_box = tkb.Entry(self)
        self.login_tag_box.grid(column=1, ipadx=10, pady=3, row=1, sticky="w")
        self.login_tag_box.bind("<Return>", self.on_login)

        self.login_password_label = tkb.Label(self)
        self.login_password_label.configure(text="Password")
        self.login_password_label.grid(column=0, padx=5, row=2, sticky="e")

        self.login_password_box = tkb.Entry(self, show="*")
        self.login_password_box.grid(column=1, ipadx=10, pady=3, row=2, sticky="w")
        self.login_password_box.bind("<Return>", self.on_login)

        self.login_btn = tkb.Button(self)
        self.login_btn.configure(text="Login")
        self.login_btn.bind("<ButtonPress>", self.on_login)
        self.login_btn.grid(column=0, columnspan=2, pady=15, row=4, sticky="nsew")

        # register
        self.register_username_label = tkb.Label(self)
        self.register_username_label.configure(text="Username")
        self.register_username_label.grid(column=2, padx=5, row=0, sticky="e")

        self.register_username_box = tkb.Entry(self)
        self.register_username_box.grid(column=3, ipadx=10, pady=3, row=0, sticky="w")
        self.register_username_box.bind("<Return>", self.on_register)

        self.register_password_label = tkb.Label(self)
        self.register_password_label.configure(text="Password")
        self.register_password_label.grid(column=2, padx=5, row=1, sticky="e")

        self.register_password_box = tkb.Entry(self, show="*")
        self.register_password_box.grid(column=3, ipadx=10, pady=3, row=1, sticky="w")
        self.register_password_box.bind("<Return>", self.on_register)

        self.register_btn = tkb.Button(self)
        self.register_btn.configure(text="Register")
        self.register_btn.bind("<ButtonPress>", self.on_register)
        self.register_btn.grid(column=2, columnspan=2, pady=15, row=3, sticky="nsew")

        self.grid_anchor("center")
        self.grid(column=0, columnspan=4, row=0, rowspan=3, sticky=tk.NSEW)

    def on_login(self, event: Event) -> None:
        """On login button press."""
        print("Login")
        # print(f"Username: {self.login_username_box.get().strip()}")
        # print(f"Tag: {self.login_tag_box.get().strip()}")
        # print(f"Password: {self.login_password_box.get().strip()}")
        username = self.login_username_box.get().strip()
        tag = int(self.login_tag_box.get().strip())
        password = self.login_password_box.get().strip()

        loop = asyncio.get_event_loop()
        success = loop.run_until_complete(self.master.connection.login(username, tag, password))
        # success = await self.master.connection.login(username, tag, password)
        if success:
            print("you are logged in!")
        else:
            print("it didnt work try again!")
        # switch to the connect frame
        self.master.switch_frame(ConnectFrame)

    def on_register(self, event: Event) -> None:
        """On login button press."""
        print("Register")
        # print(f"Username: {self.register_username_box.get().strip()}")
        # print(f"Password: {self.register_password_box.get().strip()}")
        username = self.register_username_box.get().strip()
        password = self.register_password_box.get().strip()

        loop = asyncio.get_event_loop()
        new_tag = loop.run_until_complete(self.master.connection.register(username, password))
        # new_tag = await self.master.connection.register(username, password)
        print(f'your tag is {new_tag}')


class TestFrame(tkb.Frame):
    """Frame for testing and creating."""

    def __init__(self, master):
        tkb.Frame.__init__(self, master)

        self.master = master

        self.master.title("Chat App - Test")
        pass
