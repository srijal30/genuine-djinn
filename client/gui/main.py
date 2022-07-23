import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Event
from tkinter.scrolledtext import ScrolledText


class ChatApp:
    """Main chat application GUI."""

    def __init__(self, master=None):
        # build ui
        self.mainwindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.Frame_1 = ttk.Frame(self.mainwindow)
        self.chatbox = ScrolledText(self.Frame_1)
        self.chatbox.configure(background="#c0c0c0", state="disabled")
        self.chatbox.grid(column=0, columnspan=2, row=0, rowspan=1, sticky="nsew")
        self.messagebox = ttk.Entry(self.Frame_1)
        self.message_box = tk.StringVar(value="")
        self.messagebox.configure(textvariable=self.message_box)
        self.messagebox.grid(column=0, padx=3, pady=5, row=1, sticky="nsew")
        self.messagebox.bind("<Key>", self.on_enter, add="")
        self.sendbutton = ttk.Button(self.Frame_1)
        self.sendbutton.configure(text="Send")
        self.sendbutton.grid(column=1, padx=3, pady=5, row=1, sticky="nsew")
        self.sendbutton.configure(command=self.on_send)
        self.Frame_1.configure(height=200, padding=5, width=200)
        self.Frame_1.pack(expand="true", fill="both", side="top")
        self.Frame_1.grid_anchor("center")
        self.Frame_1.rowconfigure(0, weight=1)
        self.Frame_1.columnconfigure(0, uniform=0, weight=1)
        self.mainwindow.configure(height=200, width=200)
        self.mainwindow.geometry("800x600")
        self.mainwindow.minsize(400, 300)
        self.mainwindow.resizable(True, True)
        self.mainwindow.title("Chat")

        # Main widget
        self.mainwindow = self.mainwindow

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
        self.mainwindow.quit()

    def on_about(self, payload: str) -> None:
        """About menu button."""
        print("about")

    def on_new(self, payload: str) -> None:
        """New menu button."""
        print("new")


if __name__ == "__main__":
    app = ChatApp()
    app.run()
