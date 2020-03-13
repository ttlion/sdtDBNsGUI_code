from tkinter import *
from tkinter import filedialog
from tkinter import ttk

class ElemThree:

    def __init__(self, frame, row, column, message, initStatus, maxWidth, maxWidthFilename, fileTypes ):
        self.frame = frame
        self.row = row
        self.column = column

        self.maxWidthFilename = maxWidthFilename

        self.FileName = initStatus
        self.label = ttk.Label(frame, text=message, width = maxWidth, anchor="e", style = "ask.TLabel", padding = (5,5,5,5))
        self.pathLabel = ttk.Label(frame, text = self.FileName, width = maxWidthFilename, padding = (0,5,0,5), style="filenames.TLabel")
        self.button = ttk.Button(frame, text = "Select file", command=self.getFilePath)
        self.label.grid(row=self.row, column=self.column)
        self.pathLabel.grid(row=self.row, column=self.column+1)
        self.button.grid(row=self.row, column=self.column+2, pady = 3)

        self.typesOfFiles = fileTypes


    def getFilePath(self):
        self.FileName = filedialog.askopenfilename( initialdir = ".", title = "Select file", 
                                                filetypes = self.typesOfFiles  )
        
        self.pathLabel.destroy()
        self.pathLabel = ttk.Label(self.frame, text=self.FileName, padding = (0,5,0,5), style="filenames.TLabel")
        self.pathLabel.grid(row=self.row, column=self.column+1)

    def destroy(self):
        self.label.destroy()
        self.pathLabel.destroy()
        self.button.destroy()
        
