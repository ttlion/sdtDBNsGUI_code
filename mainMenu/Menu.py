from tkinter import *

#########################################
# Menu bar class

class MyMenu:

    def __init__(self, frame):
        self.menubar = Menu(frame)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.donothing)
        self.filemenu.add_command(label="Open", command=self.donothing)
        self.filemenu.add_command(label="Save", command=self.donothing)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command=exit)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = Menu(self.menubar, tearoff=0)
        
        # edit submenu
        self.editmenu.add_command(label="Undo", command=self.donothing)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        frame.config(menu=self.menubar)

    def donothing(self):
        return
    