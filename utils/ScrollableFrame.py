# This class was adapted from https://blog.tecladocode.com/tkinter-scrollable-frames/
import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.container = container

        self.canvas = tk.Canvas(self, highlightthickness = 0, width = self.container.winfo_width()-20, height = self.container.winfo_height()-20)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", self.resize )

        # For mousewheel to work properly on all platforms
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbarX= ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=scrollbarX.set)

        scrollbar.pack(side="right", fill="y")
        scrollbarX.pack(side="bottom", fill="x")
        self.canvas.pack(side="top", fill="both", expand=True)

    def resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            direction = 1
        else:
            direction = -1
        self.canvas.yview_scroll(direction, "units")