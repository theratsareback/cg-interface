import customtkinter as ctk
import tkinter as tk

import cg_grpc
from rtsp_camera_service import VideoStream
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from cg_grpc import EventThrower, grpcclient
#from cg_grpc.client_singleton import get_client
from enum import Enum


class FurnacePage(ctk.CTkFrame):
    def on_setpoint_enter(self, event):
        value = float(self.setpoint.get())
        self.bus.set_setpoint(self.guid, value)

    def on_manual_trim_enter(self, event):
        value = float(self.manual_trim.get())
        self.bus.set_man_trim(self.guid, value)

    def on_pull_speed_enter(self, event):
        value = float(self.pull_speed.get())
        self.bus.set_steppers(value)

    def on_rotation_speed_enter(self, event):
        value = float(self.rotation_speed.get())
        self.bus.set_steppers(value)

    def select_profile(self, label):
        for profile in self.profiles:
            if profile['Label'] == label:
                self.bus.set_furnace_profile(self.guid, profile)
                return

    def set_profile_state(self, state):
        if state == "Pause": # change language to cast to enum on C# backend
            state = "Paused"
        elif state == "Resume":
            state = "Running"
        elif state == "Stop":
            state = "Stopped"
        self.bus.set_profile_status(self.guid, state)

    def enable_furnace(self):
        self.bus.enable(self.guid)

    def enable_diameter_control(self):
        self.bus.start_diameter_control(self.guid)

    def reset_diameter_control(self):
        self.bus.reset_diameter_control(self.guid)

    def set_target(self, *kwargs):
        self.bus.set_target(self.guid, [self.y_entry.get(), self.x_entry.get()]) #this looks backwards but isn't

    def set_gains(self, *kwargs):
        self.bus.set_gains(self.guid, self.kp_entry.get(), self.ki_entry.get())

    def __init__(self, guid, parent, profiles, **kwargs):
        super().__init__(parent, **kwargs)
        self.profiles = profiles
        self.guid = guid
        self.client = self.winfo_toplevel().gRPCClient
        self.bus = EventThrower.FurnaceEventBus(self.client)

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
            text= "N/A",
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

        self.setpoint = ctk.CTkLabel(
            self.left_panel,
            text="N/A",
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
        self.manual_trim.insert(0, 0)
        self.manual_trim.bind("<Return>", self.on_manual_trim_enter)

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

        # Pull Speed
        self.pull_speed_label = ctk.CTkLabel(
            self.left_panel,
            text="Pull Speed:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.pull_speed_label.grid(row=6, column=0, padx=15, pady=5, sticky="nw")

        self.pull_speed = ctk.CTkEntry(
            self.left_panel,
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.pull_speed.grid(row=6, column=1, padx=15, pady=5, sticky="nw")
        """Set a new Pull Speed for the Furnace"""
        #self.pull_speed.bind("<Return>", self.on_pull_speed_enter)

        # Rotation Speed
        self.rotation_speed_label = ctk.CTkLabel(
            self.left_panel,
            text="Rotation Speed:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.rotation_speed_label.grid(row=7, column=0, padx=15, pady=5, sticky="nw")

        self.rotation_speed = ctk.CTkEntry(
            self.left_panel,
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.rotation_speed.grid(row=7, column=1, padx=15, pady=5, sticky="nw")
        """Set a new Rotation Speed for the Furnace"""
        #self.rotation_speed.bind("<Return>", self.on_rotation_speed_enter)

        # Profile Control
        self.profileStatus_label = ctk.CTkLabel(
            self.left_panel,
            text="Profile Status:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.profileStatus_label.grid(row=8, column=0, padx=15, pady=5, sticky="nw")

        self.profileStatus = ctk.CTkSegmentedButton(
            self.left_panel,
            values=["Pause", "Resume", "Stop"],
            font=("Arial", 18),
            text_color="white",
            command=self.set_profile_state,
        )
        self.profileStatus.grid(row=8, column=1, padx=15, pady=5, sticky="nw")

        # Profile Selection
        self.profile_selection_label = ctk.CTkLabel(
            self.left_panel,
            text="Profile:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.profile_selection_label.grid(row=9, column=0, padx=15, pady=5, sticky="nw")

        self.profile_selection = ctk.CTkOptionMenu(
            self.left_panel,
            values=[x['Label'] for x in self.profiles],
            font=("Arial", 18),
            text_color = "white",
            command=self.select_profile,
        )
        self.select_profile(self.profile_selection._values[0]) # actually select default
        self.profile_selection.grid(row=9, column=1, padx=15, pady=5, sticky="nw")

        # Enable/Disable
        self.status = ctk.CTkButton(
            self.left_panel,
            text="Toggle Furnace",
            text_color="white",
            font=("Arial", 18),
            command=self.enable_furnace
        )
        self.status.grid(row=10, column=0, padx=15, pady=15, sticky="nw")

        # Acknowledge Alarms
        self.a_alarms = ctk.CTkButton(
            self.left_panel,
            text="Acknowledge Alarms",
            text_color = "white",
            font=("Arial", 18),
        )
        self.a_alarms.grid(row=10, column=1, padx=15, pady=15, sticky="nw")

        # diameter control
        self.dcEnable = ctk.CTkButton(
            self.left_panel,
            text="Start Diameter Control",
            text_color="white",
            font=("Arial", 18),
            command=self.enable_diameter_control
        )
        self.dcEnable.grid(row=11, column=0, padx=15, pady=15, sticky="nw")

        self.dcReset = ctk.CTkButton(
            self.left_panel,
            text="Reset Diameter Control",
            text_color="white",
            font=("Arial", 18),
            command=self.reset_diameter_control
        )
        self.dcReset.grid(row=11, column=1, padx=15, pady=15, sticky="nw")

        # target control
        self.x_entry_label = ctk.CTkLabel(
            self.left_panel,
            text="Target X position:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.x_entry_label.grid(row=12, column=0, padx=15, pady=5, sticky="nw")

        self.x_entry = ctk.CTkEntry(
            self.left_panel,
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.x_entry.grid(row=13, column=1, padx=15, pady=5, sticky="nw")
        self.x_entry.insert(0, 0)
        self.x_entry.bind("<Return>", self.set_target)

        self.y_entry_label = ctk.CTkLabel(
            self.left_panel,
            text="Target Y position:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.y_entry_label.grid(row=13, column=0, padx=15, pady=5, sticky="nw")

        self.y_entry = ctk.CTkEntry(
            self.left_panel,
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.y_entry.grid(row=12, column=1, padx=15, pady=5, sticky="nw")
        self.y_entry.insert(0, 0)
        self.y_entry.bind("<Return>", self.set_target)

        # gain control
        self.kp_entry_label = ctk.CTkLabel(
            self.left_panel,
            text="kp:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.kp_entry_label.grid(row=14, column=0, padx=15, pady=5, sticky="nw")

        self.kp_entry = ctk.CTkEntry(
            self.left_panel,
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.kp_entry.grid(row=14, column=1, padx=15, pady=5, sticky="nw")
        self.kp_entry.insert(0, 0)
        self.kp_entry.bind("<Return>", self.set_gains)

        self.ki_entry_label = ctk.CTkLabel(
            self.left_panel,
            text="ki:",
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.ki_entry_label.grid(row=15, column=0, padx=15, pady=5, sticky="nw")

        self.ki_entry = ctk.CTkEntry(
            self.left_panel,
            font=("Arial", 18),
            text_color="white",
            justify="left",
        )
        self.ki_entry.grid(row=15, column=1, padx=15, pady=5, sticky="nw")
        self.ki_entry.insert(0, 0)
        self.ki_entry.bind("<Return>", self.set_gains)

        # -- RIGHT PANEL -- #

        self.right_panel = ctk.CTkFrame(
            self.paned,
            fg_color="#2b2b2b",
            corner_radius=0,
        )
        self.paned.add(self.right_panel, minsize=400)

        self.camera_view = VideoStream(
            self.right_panel,
            rtsp_url="rtsp://192.168.168.103:8554/cam",
        )
        self.camera_view.pack(side="top", fill="both", expand=True, pady=(0, 10))

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
        self.process_value.configure(text=f"{round(newState["processValue"],2 )}")
        self.dc_trim.configure(text=f"{round(newState["diameterTrim"],2 )}")
        self.setpoint.configure(text=f"{round(newState["setpoint"],2 )}")
        #todo implement state storage in new furnace container class