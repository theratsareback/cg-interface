import customtkinter as ctk
import uuid
import json

from cg_grpc import EventThrower
from .tab_button import TabButton
from .furnace_page import FurnacePage


class MainWindow(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.tabs = {}
        self.profiles = None
        self.pages = {}
        self.current = None

        self.tab_bar = ctk.CTkFrame(self, fg_color="#1f1f1f", corner_radius=0)
        self.tab_bar.grid(row=0, column=0, sticky="ns", padx=(0, 0))

        self.tab_bar.grid_propagate(False)
        self.tab_bar.configure(width=140)
        self.tab_bar.grid_rowconfigure(0, weight=1)

        self.page_container = ctk.CTkFrame(self, fg_color="#1f1f1f", corner_radius=0)
        self.page_container.grid(row=0, column=1, sticky="nsew", padx=(0, 0))
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

    def get_profiles(self):
        client = self.winfo_toplevel().gRPCClient
        bus = EventThrower.FurnaceEventBus(client)
        self.profiles = json.loads(bus.request_profiles().payload)


    def add_tab(self, guid, name, **page_kwargs):
        tab = TabButton(
            self.tab_bar,
            guid,
            text=name,
            command=lambda g=guid: self.show_tab(g)
        )
        tab.pack(pady=(2, 2), padx=10, fill="x")

        page = FurnacePage(guid, self.page_container, self.profiles)
        page.grid(row=0, column=0, sticky="nsew")

        self.tabs[guid] = tab
        self.pages[guid] = page

        # Show first tab
        if self.current is None:
            self.show_tab(guid)
        else:
            self.pages[self.current].lift()

    def show_tab(self, guid):
        if self.current == guid:
            return

        if self.current is not None:
            self.tabs[self.current].deselect()

        self.current = guid
        self.pages[guid].lift()
        self.tabs[guid].select()

    def gRPCupdate(self, newFrame):
        payload = newFrame.payload
        updateDict = json.loads(payload)

        for guid in updateDict:
            if self.tabs.get(guid) is not None:
                self.tabs[guid].gRPCupdate(updateDict[guid])
                self.pages[guid].gRPCupdate(updateDict[guid])
            else:
                self.add_tab(guid, updateDict[guid]["furnaceLabel"])
                self.tabs[guid].gRPCupdate(updateDict[guid])
                self.pages[guid].gRPCupdate(updateDict[guid])

    def add_test_tab(self, label):
        guid = uuid.uuid4()
        self.add_tab(guid, label)