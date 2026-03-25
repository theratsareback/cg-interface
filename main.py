import tkinter as tk
import time
from tkinter import ttk
import views
import services

from cg_grpc import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Isomet CG Interface")
        self.geometry("1920x1080")
        self._configure_styles()

        self.main = views.MainWindow(self, style="TabBar.TFrame")
        self.main.pack(fill="both", expand=True, padx=10, pady=10)

        self.client = FurnaceGrpcClient(
            "192.168.168.103:5000",
            on_frame_received=self.on_frame_received,
        )
        self.client.start()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_frame_received(self, frame: Frame) -> None:
        self.after(0, self._apply_frame, frame)

    def _apply_frame(self, frame: Frame) -> None:
        self.main.gRPCupdate(frame)

    def on_close(self) -> None:
        self.client.close()
        self.destroy()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TabButton.TFrame",
            background="#ffffff",
            relief="flat",
            borderwidth=1
        )
        style.map(
            "TabButton.TFrame",
            background=[
                ("selected", "#d9d9d9"),
                ("pressed", "#cfcfcf"),
                ("active", "#e6e6e6"),
            ]
        )

        style.configure(
            "Page.TFrame",
            background="#d9d9d9",
            relief="groove",
            borderwidth=0.5
        )

        style.configure(
            "TabButton.TLabel",
            background="#ffffff"
        )
        style.map(
            "TabButton.TLabel",
            background=[
                ("selected", "#d9d9d9"),
                ("pressed", "#cfcfcf"),
                ("active", "#e6e6e6"),
            ]
        )

        style.configure(
            "TabBar.TFrame",
            background="#d9d9d9",
            relief="flat",
            borderwidth=1
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()