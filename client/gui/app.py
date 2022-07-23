import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Event, IntVar, Menu
from tkinter.scrolledtext import ScrolledText

import ttkbootstrap as tkb

# from ttkbootstrap.constants import DARK

__all__ = (
    "ChatApp"
)


class ChatApp:
    """Main chat application GUI."""

    def __init__(self, master=None):
        # build ui
        self.main_window = tkb.Window(themename="darkly")  # darkly/flatly
        self.main_window.configure(height=200, width=200)
        self.main_window.geometry("800x600")
        self.main_window.minsize(400, 300)
        self.main_window.resizable(True, True)
        self.main_window.title("Chat App")

        # chat frame
        self.chat_frame = ttk.Frame(self.main_window)
        self.chatbox = ScrolledText(self.chat_frame)
        self.chatbox.configure(state="disabled")
        self.chatbox.grid(column=0, columnspan=2, row=0, rowspan=1, sticky="nsew")
        self.messagebox = ttk.Entry(self.chat_frame)
        self.message_box = tk.StringVar(value="")
        self.messagebox.configure(textvariable=self.message_box)
        self.messagebox.grid(column=0, padx=3, pady=5, row=1, sticky="nsew")
        self.messagebox.bind("<Key>", self.on_enter, add="")
        self.sendbutton = tkb.Button(self.chat_frame)
        self.sendbutton.configure(text="Send")
        self.sendbutton.grid(column=1, padx=3, pady=5, row=1, sticky="nsew")
        self.sendbutton.configure(command=self.on_send)
        self.chat_frame.configure(height=200, padding=5, width=200)
        self.chat_frame.pack(expand="true", fill="both", side="top")
        self.chat_frame.grid_anchor("center")
        self.chat_frame.rowconfigure(0, weight=1)
        self.chat_frame.columnconfigure(0, uniform=0, weight=1)

        # menu bar
        self.menubar = Menu(self.main_window)

        # file menu
        filemenu = Menu(self.menubar, tearoff=False)
        filemenu.add_command(label="Leave Room", command=None)
        filemenu.add_command(label="Log Out", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.main_window.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        # edit menu
        editmenu = Menu(self.menubar, tearoff=False)

        sizemenu = Menu(editmenu, tearoff=False)
        sizemenu.add_radiobutton(label="Small", value=1, variable=IntVar)
        sizemenu.add_radiobutton(label="Medium", value=1, variable=IntVar)
        sizemenu.add_radiobutton(label="Large", value=1, variable=IntVar)
        editmenu.add_cascade(label="Text Size", menu=sizemenu)

        thememenu = Menu(editmenu, tearoff=False)
        thememenu.add_radiobutton(label="Light", value=1, variable=IntVar)
        thememenu.add_radiobutton(label="Dark", value=1, variable=IntVar)
        editmenu.add_cascade(label="Theme", menu=thememenu)

        self.menubar.add_cascade(label="Edit", menu=editmenu)

        # help menu
        helpmenu = Menu(self.menubar, tearoff=False)
        helpmenu.add_command(label="About", command=None)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        # add menu to frame
        self.main_window.config(menu=self.menubar)

    def run(self) -> None:
        """Start GUI window loop."""
        self.main_window.mainloop()

    def on_enter(self, event: Event) -> None:
        """Clicking enter in messagebox."""
        if event.keysym == "Return":
            self.is_valid()

    def on_send(self) -> None:
        """Clicking send button."""
        self.is_valid()

    def is_valid(self) -> None:
        """Is the message valid to send?"""
        message = self.messagebox.get().strip()

        if len(message) > 0:
            self.send(message)

    def send(self, message: str) -> None:
        """Sends chat message."""
        print(message)
        self.message_box.set("")
        self.display(message)

    def display(self, message: str) -> None:
        """Displays chat message."""
        self.chatbox.configure(state="normal")
        self.chatbox.insert("end", f"{message}\n")
        self.chatbox.configure(state="disable")
        self.chatbox.yview_moveto(1)

    def on_quit(self, payload: str) -> None:
        """Quit menu button."""
        print("quit")
        self.main_window.quit()

    def on_about(self, payload: str) -> None:
        """About menu button."""
        print("about")

    def on_new(self, payload: str) -> None:
        """New menu button."""
        print("new")
