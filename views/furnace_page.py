from tkinter import ttk
from rtsp_camera_service import VideoStream
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

        # Graph
        bg_color = self.winfo_toplevel().cget("background")

        self.fig = Figure(figsize=(4, 4), dpi=100, facecolor=bg_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Graph")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(side="top", fill="both", expand=True)

    def gRPCupdate(self, newState):
        self.label.configure(text=f"Process Value: {newState["processValue"]}")
        #todo implement state storage in new furnace container class