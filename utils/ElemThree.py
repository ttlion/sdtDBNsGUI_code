from tkinter import *
from tkinter import filedialog

class ElemThree:

    def __init__(self, frame, row, column, message, initStatus, maxWidth ):
        self.frame = frame
        self.row = row
        self.column = column

        self.FileName = initStatus
        self.label = Label(frame, text=message, width=maxWidth, anchor="e")
        self.pathLabel = Label(frame, text=self.FileName)
        self.button = Button(frame, text = "Select file", padx=25, pady=15, command=self.getFilePath)
        self.label.grid(row=self.row, column=self.column)
        self.pathLabel.grid(row=self.row, column=self.column+1)
        self.button.grid(row=self.row, column=self.column+2)


    def getFilePath(self):
        self.FileName = filedialog.askopenfilename( initialdir = ".", title = "Select file", 
                                                filetypes = [("csv files", "*.csv" )]  )
        
        self.pathLabel.destroy()
        self.pathLabel = Label(self.frame, text=self.FileName)
        self.pathLabel.grid(row=self.row, column=self.column+1)

    def destroy(self):
        self.label.destroy()
        self.pathLabel.destroy()
        self.button.destroy()
        
