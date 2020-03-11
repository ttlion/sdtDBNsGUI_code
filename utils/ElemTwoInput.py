from tkinter import *
from tkinter import ttk

class ElemTwoInput:

    def __init__(self, frame, message, maxWidthText, maxWidthEntry, row, column, defaultValue):
        self.frame = frame
        self.row = row
        self.column = column

        self.label = ttk.Label(frame, text = message, width = maxWidthText, anchor = "e", style = "ask.TLabel")
        self.label.grid(row=self.row, column = self.column)

        self.entry = ttk.Entry(frame, width = maxWidthEntry, justify="left", font=("Times", 11, "bold"))
        self.entry.insert(0, defaultValue)
        self.entry.grid(row=self.row, column = self.column+1, sticky="W", pady = 3)
    
    def destroy(self):
        self.label.destroy()
        self.entry.destroy()

