import pathlib
from tkinter import Event

import pygubu  # type: ignore

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "chat.ui"


class GUI:
    """Main GUI window."""

    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        self.mainwindow = builder.get_object("mainwindow", master)

        self.mainmenu = builder.get_object("mainmenu", self.mainwindow)
        self.mainwindow.configure(menu=self.mainmenu)

        builder.connect_callbacks(self)

    def run(self) -> None:
        """Start GUI window loop."""
        self.mainwindow.mainloop()

    def on_enter(self, event: Event) -> None:
        """Clicking enter in messagebox."""
        if event.keysym == "Return":
            self.is_valid()

    def on_send(self) -> None:
        """Clicking send button."""
        self.is_valid()

    def is_valid(self) -> None:
        """Is the message valid to send?"""
        messagebox = self.builder.get_object("messagebox")
        message = messagebox.get().strip()

        if len(message) > 0:
            self.send(message)

    def send(self, message: str) -> None:
        """Sends chat message."""
        print(message)

        messagebox = self.builder.get_variable("message_box")
        messagebox.set("")

        self.display(message)

    def display(self, message: str) -> None:
        """Displays chat message."""
        chatcontent = self.builder.get_object("chatbox")
        chatcontent.configure(state="normal")
        chatcontent.insert("end", f"{message}\n")
        chatcontent.configure(state="disable")
        chatcontent.yview_moveto(1)

    def on_quit(self, payload: str) -> None:
        """Quit menu button."""
        print("quit")
        self.mainwindow.quit()

    def on_about(self, payload: str) -> None:
        """About menu button."""
        print("about")

    def on_new(self, payload: str) -> None:
        """New menu button."""
        print("new")


if __name__ == "__main__":
    app = GUI()
    app.run()
