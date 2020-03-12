from tkinter import *
from tkinter import ttk

class ElemTwoInputPresent:

    def __init__(self, frame, messageLeft, messageRight, maxWidthLeft, maxWidthRight, row, column):
        self.frame = frame
        self.row = row
        self.column = column

        self.messageLeft = messageLeft
        self.messageRight = messageRight

        self.labelLeft = ttk.Label(frame, text = messageLeft, width = maxWidthLeft, anchor = "e", style = "ask.TLabel")
        self.labelLeft.grid(row = self.row, column = self.column)

        self.labelRight = ttk.Label(frame, text = messageRight, width = maxWidthRight, anchor = "w", style = "filenames.TLabel")
        self.labelRight.grid(row = self.row, column = self.column + 1)
    
    def destroy(self):
        self.labelLeft.destroy()
        self.labelRight.destroy()

