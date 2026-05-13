import customtkinter as ctk
import time
import views
#from cg_grpc.client_singleton import get_client, make_client


from cg_grpc import *

_client = None

def get_client():
    global _client
    return _client

def make_client(func):

    global _client

    if _client is None:
        _client = FurnaceGrpcClient(
            "192.168.168.103:5000",
            on_frame_received=lambda frame: func(frame)
        )
        _client.start()

    return _client

# Configure global appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.gRPCClient = None
        self.title("Isomet CG Interface")
        self.geometry("1920x1080")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main = views.MainWindow(self)
        self.main.grid(row=0, column=0, sticky="nsew")

        # self.main.add_test_tab("Test Furnace 1")
        # self.main.add_test_tab("Test Furnace 2")
        # self.main.add_test_tab("Test Furnace 3")


        self.gRPCClient = make_client(self._apply_frame)


        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_frame_received(self, frame):
        # Use after(0) to schedule on main thread
        self.after(0, self._apply_frame, frame)

    def _apply_frame(self, frame):
        self.main.gRPCupdate(frame)

    def on_close(self):
        if self.gRPCClient is not None:
            self.gRPCClient.close()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()