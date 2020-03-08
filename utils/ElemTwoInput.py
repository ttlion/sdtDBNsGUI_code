from tkinter import *

class ElemTwoInput:

    def __init__(self, frame, message, maxWidthText, maxWidthEntry, row, column):
        self.frame = frame
        self.row = row
        self.column = column

        self.label = Label(frame, text=message, width=maxWidthText, anchor="e")
        self.label.grid(row=self.row, column=self.column)

        self.entry = Entry(frame, width=maxWidthEntry, borderwidth=3, justify="left")
        self.entry.insert(0, 1)
        self.entry.grid(row=self.row, column=self.column+1, sticky="W")
    
    def destroy(self):
        self.label.destroy()
        self.entry.destroy()

