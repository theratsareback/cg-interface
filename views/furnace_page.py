import customtkinter as ctk
import tkinter as tk
from rtsp_camera_service import VideoStream
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class FurnacePage(ctk.CTkFrame):
    def __init__(self, guid, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.guid = guid

        self.paned = tk.PanedWindow(
            self,
            orient="horizontal",
            sashwidth=2,
            sashrelief="flat",
            bg="#3d3d3d",
            handlepad=0,
            opaqueresize=True,
        )
        self.paned.pack(fill="both", expand=True)

        self.left_panel = ctk.CTkFrame(
            self.paned,
            fg_color="#2b2b2b",
            corner_radius=0,
        )
        self.paned.add(self.left_panel, minsize=1000)

        self.left_panel.grid_rowconfigure(0, weight=0)
        self.left_panel.grid_columnconfigure(0, weight=0)
        self.left_panel.grid_columnconfigure(1, weight=0)
        self.left_panel.grid_columnconfigure(2, weight=0)
        self.left_panel.grid_columnconfigure(3, weight=1)

        # Process value
        self.label = ctk.CTkLabel(
            self.left_panel,
            text="Process Value:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.label.grid(row=1, column=0, padx=15, pady=5, sticky="nw")

        self.process_value = ctk.CTkLabel(
            self.left_panel,
            text="N/A",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.process_value.grid(row=1, column=1, padx=15, pady=5, sticky="nw")

        # Setpoint
        self.setpoint_label = ctk.CTkLabel(
            self.left_panel,
            text="Setpoint:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.setpoint_label.grid(row=3, column=0, padx=15, pady=5, sticky="nw")

        self.setpoint = ctk.CTkEntry(
            self.left_panel,
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.setpoint.grid(row=3, column=1, padx=15, pady=5, sticky="nw")

        # Manual trim
        self.manual_trim_label = ctk.CTkLabel(
            self.left_panel,
            text="Manual Trim:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.manual_trim_label.grid(row=4, column=0, padx=15, pady=5, sticky="nw")

        self.manual_trim = ctk.CTkEntry(
            self.left_panel,
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.manual_trim.grid(row=4, column=1, padx=15, pady=5, sticky="nw")

        # Diameter control trim
        self.dc_trim_label = ctk.CTkLabel(
            self.left_panel,
            text="Diameter Control Trim:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.dc_trim_label.grid(row=5, column=0, padx=15, pady=5, sticky="nw")

        self.dc_trim = ctk.CTkLabel(
            self.left_panel,
            text="N/A",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.dc_trim.grid(row=5, column=1, padx=15, pady=5, sticky="nw")

        # Profile Control
        self.profileStatus_label = ctk.CTkLabel(
            self.left_panel,
            text="Profile Status:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.profileStatus_label.grid(row=6, column=0, padx=15, pady=5, sticky="nw")

        self.profileStatus = ctk.CTkSegmentedButton(
            self.left_panel,
            values=["Pause", "Resume", "Stop"],
            font=("Arial", 18),
            text_color="white",
        )
        self.profileStatus.grid(row=6, column=1, padx=15, pady=5, sticky="nw")

        # Profile Selection
        self.profile_selection_label = ctk.CTkLabel(
            self.left_panel,
            text="Profile:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.profile_selection_label.grid(row=7, column=0, padx=15, pady=5, sticky="nw")

        self.profile_selection = ctk.CTkOptionMenu(
            self.left_panel,
            values=["Test Profile 1", "Test Profile 2"],
            font=("Arial", 18),
            text_color = "white",
        )
        self.profile_selection.grid(row=7, column=1, padx=15, pady=5, sticky="nw")

        # Enable/Disable
        self.status = ctk.CTkButton(
            self.left_panel,
            text="Toggle Furnace",
            text_color="white",
            font=("Arial", 18),
        )
        self.status.grid(row=8, column=0, padx=15, pady=15, sticky="nw")

        # Acknowledge Alarms
        self.a_alarms = ctk.CTkButton(
            self.left_panel,
            text="Acknowledge Alarms",
            text_color = "white",
            font=("Arial", 18),
        )
        self.a_alarms.grid(row=8, column=1, padx=15, pady=15, sticky="nw")

        # -- RIGHT PANEL -- #

        self.right_panel = ctk.CTkFrame(
            self.paned,
            fg_color="#2b2b2b",
            corner_radius=0,
        )
        self.paned.add(self.right_panel, minsize=400)

        self.camera_view = VideoStream(
            self.right_panel,
            rtsp_url="rtsp://192.168.168.202:8554/cam",
            width=640,
            height=480,
        )
        self.camera_view.pack(side="top", fill="x", pady=(0, 10))

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.fig.patch.set_facecolor("#2b2b2b")
        plot_bg_color = "#3a3a3a"
        self.ax.set_facecolor(plot_bg_color)

        self.ax.tick_params(colors="white", direction="in", length=6, width=1)
        self.ax.xaxis.label.set_color("white")
        self.ax.yaxis.label.set_color("white")
        self.ax.title.set_color("white")

        for spine in self.ax.spines.values():
            spine.set_color("white")
            spine.set_linewidth(1)

        self.ax.set_title("Graph")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(side="top", fill="both", expand=True)

        self.canvas.draw()

    def gRPCupdate(self, newState):
        self.label.configure(text=f"Process Value: {newState["processValue"]}")
        #todo implement state storage in new furnace container class