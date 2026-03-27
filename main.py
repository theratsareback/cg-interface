import tkinter as tk
import time
from tkinter import ttk
import views

from cg_grpc import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gRPCClient = None
        self.title("Isomet CG Interface")
        self.geometry("1920x1080")
        self._configure_styles()

        self.main = views.MainWindow(self, style="TabBar.TFrame")
        self.main.pack(fill="both", expand=True, padx=10, pady=10)

        self.main.add_test_tab("Test Furnace 1")
        self.main.add_test_tab("Test Furnace 2")
        self.main.add_test_tab("Test Furnace 3")

        """
        self.gRPCClient = FurnaceGrpcClient(
            "192.168.168.103:5000",
            on_frame_received=self.on_frame_received,
        )
        self.gRPCClient.start()
        """

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_frame_received(self, frame: Frame) -> None:
        self.after(0, self._apply_frame, frame)

    def _apply_frame(self, frame: Frame) -> None:
        self.main.gRPCupdate(frame)

    def on_close(self) -> None:
        if self.gRPCClient is not None:
            self.gRPCClient.close()
        self.destroy()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TabButton.TFrame",
            background="#d9d9d9",
            relief="flat",
            borderwidth=1
        )
        style.map(
            "TabButton.TFrame",
            background=[
                ("selected", "#ffffff"),
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
            background="#d9d9d9"
        )
        style.map(
            "TabButton.TLabel",
            background=[
                ("selected", "#ffffff"),
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