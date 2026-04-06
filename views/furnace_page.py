from tkinter import ttk
from rtsp_camera_service import VideoStream

class FurnacePage(ttk.Frame):
    def __init__(self, guid, parent, **kwargs):
        super().__init__(parent, padding=20, **kwargs)
        self.label = ttk.Label(self, text="Process Value:")
        self.label.pack()
        self.guid = guid
        #todo implement UI

        # Camera stream
        self.camera_view = VideoStream(
            self,
            rtsp_url="rtsp://192.168.168.202:8554/cam",
            width=1280,
            height=720
        )
        self.camera_view.pack(pady=10)

    def gRPCupdate(self, newState):
        self.label.configure(text=f"Process Value: {newState["processValue"]}")
        #todo implement state storage in new furnace container class