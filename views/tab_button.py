from tkinter import ttk

class TabButton(ttk.Frame):
    def __init__(self, guid, parent, text, command, **kwargs):
        super().__init__(parent, style="TabButton.TFrame", padding=(12, 8), **kwargs)
        self.command = command
        self.guid = guid

        self.label = ttk.Label(self, text=text, style="TabButton.TLabel")
        self.label.pack()

        for widget in (self, self.label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<ButtonPress-1>", self._on_press)
            widget.bind("<ButtonRelease-1>", self._on_release)

        #todo add on-tab status indicators

    def _on_enter(self, event):
        if "selected" not in self.state():
            self.state(["active"])
            self.label.state(["active"])

    def _on_leave(self, event):
        if "selected" not in self.state():
            self.state(["!active", "!pressed"])
            self.label.state(["!active", "!pressed"])

    def _on_press(self, event):
        if "selected" not in self.state():
            self.state(["pressed"])
            self.label.state(["pressed"])

    def _on_release(self, event):
        if "selected" not in self.state():
            self.state(["!pressed"])
            self.label.state(["!pressed"])
            self.command()

    def select(self):
        self.state(["selected", "!active", "!pressed"])
        self.label.state(["selected", "!active", "!pressed"])

    def deselect(self):
        self.state(["!selected", "!active", "!pressed"])
        self.label.state(["!selected", "!active", "!pressed"])

    def gRPCupdate(self, newState):
        pass
        #todo implement