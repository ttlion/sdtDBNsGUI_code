from tkinter import *
from tkinter import ttk

class ElemTwoSelect:

    def __init__(self, frame, message, maxWidthText, tkVar, choices, defaultChoice, row, column):
        self.frame = frame
        self.row = row
        self.column = column

        self.tkVar = tkVar
        self.tkVar.set(defaultChoice)
        self.choices = choices

        self.label = ttk.Label(frame, text=message, width = maxWidthText, anchor="e", style="ask.TLabel")
        self.label.grid(row=self.row, column=self.column)

        self.menu = ttk.OptionMenu(frame, self.tkVar, defaultChoice, *self.choices)
        self.menu.grid(row=self.row, column=self.column+1, sticky="W", pady = 3)

    def destroy(self):
        self.label.destroy()
        self.menu.destroy()
