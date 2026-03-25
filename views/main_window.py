import tkinter as tk
from tkinter import ttk
from cg_grpc import *
import json

from .tab_button import TabButton
from .furnace_page import FurnacePage

class MainWindow(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.tabs = {}
        self.pages = {}
        self.current = None

        self.tab_bar = ttk.Frame(self)
        self.tab_bar.pack(side="left", fill="y")

        self.page_container = ttk.Frame(self)
        self.page_container.pack(side="top", fill="both", expand=True)

        # stack all pages in the same cell
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

    def add_tab(self, guid, name, page_class, **page_kwargs):
        # Create button
        tab = TabButton(
            guid,
            self.tab_bar,
            text=name,
            command=lambda g=guid: self.show_tab(g)
        )
        tab.pack(side="top", padx=(0, 2))

        # Create page
        page = page_class(guid, self.page_container, style = "Page.TFrame")
        page.grid(row=0, column=0, sticky="nsew")

        self.tabs[guid] = tab
        self.pages[guid] = page

        # Show first tab
        if self.current is None:
            self.show_tab(guid)

    def show_tab(self, guid):
        if self.current == guid:
            return

        if self.current is not None:
            self.tabs[self.current].deselect()

        self.current = guid
        self.pages[guid].tkraise()
        self.tabs[guid].select()

    def gRPCupdate(self, newFrame: Frame):
        payload = newFrame.payload
        updateDict = json.loads(payload)

        for guid in updateDict:
            if self.tabs.get(guid) is not None:
                self.tabs[guid].gRPCupdate(updateDict[guid])
                self.pages[guid].gRPCupdate(updateDict[guid])

            else:
                self.add_tab(guid, updateDict[guid]["furnaceLabel"], FurnacePage)
                self.tabs[guid].gRPCupdate(updateDict[guid])
                self.pages[guid].gRPCupdate(updateDict[guid])