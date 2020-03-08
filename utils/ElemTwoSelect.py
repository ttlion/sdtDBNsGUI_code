from tkinter import *

class ElemTwoSelect:

    def __init__(self, frame, message, maxWidthText, tkVar, choices, defaultChoice, row, column):
        self.frame = frame
        self.row = row
        self.column = column

        self.tkVar = tkVar
        self.tkVar.set(defaultChoice)
        self.choices = choices


        self.label = Label(frame, text=message, width=maxWidthText, anchor="e")
        self.label.grid(row=self.row, column=self.column)

        self.menu = OptionMenu(frame, self.tkVar, *self.choices)
        self.menu.grid(row=self.row, column=self.column+1, sticky="W")

    def destroy(self):
        self.label.destroy()
        self.menu.destroy()
