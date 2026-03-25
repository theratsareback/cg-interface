from tkinter import ttk

class FurnacePage(ttk.Frame):
    def __init__(self, guid, parent, **kwargs):
        super().__init__(parent, padding=20, **kwargs)
        self.label = ttk.Label(self, text="Process Value:")
        self.label.pack()
        self.guid = guid
        #todo implement UI

    def gRPCupdate(self, newState):
        self.label.configure(text=f"Process Value: {newState["processValue"]}")
        #todo implement state storage in new furnace container class