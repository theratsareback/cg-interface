import customtkinter as ctk

class TabButton(ctk.CTkFrame):
    def __init__(self, parent, guid, text, command):
        super().__init__(
            parent,
            fg_color="transparent",
            corner_radius=5,
            height=40,
            cursor="hand2",
        )
        self.guid = guid
        self.command = command
        self.is_selected = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=("Arial", 14),
            text_color="white",
            anchor="w",
        )
        self.label.grid(row=0, column=0, sticky="ew", padx=(15, 5))

        self.furnaceStatus = ctk.CTkLabel(
            self,
            text="",
            width=20,
            height=20,
            corner_radius=10,
            fg_color="red",
        )
        self.furnaceStatus.grid(row=0, column=1, padx=(5, 15), pady=10)

        for widget in [self, self.furnaceStatus, self.label]:
            widget.bind("<Button-1>", lambda e: self._handle_click())

    def set_status(self, color):
        self.furnaceStatus.configure(fg_color=color)

    def _handle_click(self):
        if not self.is_selected:
            self.command()

    def select(self):
        self.is_selected = True
        self.configure(fg_color="#2b5a8c")
        self.label.configure(text_color="white")

    def deselect(self):
        self.is_selected = False
        self.configure(fg_color="transparent")
        self.label.configure(text_color="gray")

    def gRPCupdate(self, newState):
        pass
        # todo implement
