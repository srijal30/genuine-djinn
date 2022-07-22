import pathlib

import pygubu  # type: ignore

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "chat.ui"


class GUI:
    """Main application GUI class"""

    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("mainwindow", master)
        builder.connect_callbacks(self)

    def run(self):
        """Starts main GUI window"""
        self.mainwindow.mainloop()

    def on_enter(self, callback):
        """On clicking enter while in messagebox"""
        if callback.keysym == "Return":
            self.is_valid()

    def on_send(self):
        """On clicking send button"""
        self.is_valid()

    def is_valid(self):
        """Is the message valid to send?"""
        messagebox = self.builder.get_object("messagebox")
        message = messagebox.get().strip()

        # message length > 0
        if len(message) > 0:
            self.send(message)

    def send(self, message):
        """Sends chat message"""
        print(message)

        # Clear text in message box
        messagebox = self.builder.get_variable("message_box")
        messagebox.set("")

        self.display(message)

    def display(self, message):
        """Displays a chat message"""
        chatcontent = self.builder.get_object("chatbox")
        chatcontent.configure(state="normal")
        chatcontent.insert("end", f"{message}\n")
        chatcontent.configure(state="disable")


if __name__ == "__main__":
    app = GUI()
    app.run()
