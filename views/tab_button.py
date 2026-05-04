import customtkinter as ctk

class TabButton(ctk.CTkButton):
    def __init__(self, parent, guid, text, command):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color="transparent",
            hover_color="#3a7ebf",
            corner_radius=5,
            height=40,
        )
        self.guid = guid
        self.is_selected = False

        self._original_command = command
        self.configure(command=self._handle_click)

    def _handle_click(self):
        if not self.is_selected:
            self._original_command()

    def select(self):
        self.is_selected = True
        self.configure(fg_color="#2b5a8c")  # Selected color
        self.configure(text_color="white")

    def deselect(self):
        self.is_selected = False
        self.configure(fg_color="transparent")
        self.configure(text_color="gray")
