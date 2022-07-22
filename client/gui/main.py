import pathlib

import pygubu  # type: ignore

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "chat.ui"


class GUI:
    """Main GUI window."""

    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Main widget
        self.mainwindow = builder.get_object("mainwindow", master)

        # Set main menu
        self.mainmenu = builder.get_object("mainmenu", self.mainwindow)
        self.mainwindow.configure(menu=self.mainmenu)

        builder.connect_callbacks(self)

    def run(self):
        """Start GUI window loop."""
        self.mainwindow.mainloop()

    def on_enter(self, callback):
        """Clicking enter in messagebox."""
        if callback.keysym == "Return":
            self.is_valid()

    def on_send(self):
        """Clicking send button."""
        self.is_valid()

    def is_valid(self):
        """Is the message valid to send?"""
        messagebox = self.builder.get_object("messagebox")
        message = messagebox.get().strip()

        if len(message) > 0:
            self.send(message)

    def send(self, message):
        """Sends chat message."""
        print(message)

        messagebox = self.builder.get_variable("message_box")
        messagebox.set("")

        self.display(message)

    def display(self, message):
        """Displays chat message."""
        chatcontent = self.builder.get_object("chatbox")
        chatcontent.configure(state="normal")
        chatcontent.insert("end", f"{message}\n")
        chatcontent.configure(state="disable")
        chatcontent.yview_moveto(1)

    def on_quit(self, payload):
        """Quit menu button."""
        print("quit")
        self.mainwindow.quit()

    def on_about(self, payload):
        """About menu button."""
        print("about")

    def on_new(self, payload):
        """New menu button."""
        print("new")


if __name__ == "__main__":
    app = GUI()
    app.run()
