from tkinter import *
import sys
import webbrowser

#########################################
# Menu bar class

class MyMenu:

    def __init__(self, frame):
        self.menubar = Menu(frame)
        self.filemenu = Menu(self.menubar, tearoff=0)

        # Uncomment this to add options to "File" submenu
        # self.filemenu.add_command(label="New", command=self.donothing)
        # self.filemenu.add_command(label="Open", command=self.donothing)
        # self.filemenu.add_command(label="Save", command=self.donothing)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command=sys.exit)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        
        # "Help" submenu
        self.helpmenu.add_command(label="sdtDBNs webpage", command=self.gotoWebpage_sdtDBN)
        self.helpmenu.add_command(label="sdtDBNs Github project", command=self.gotoRepo_sdtDBN)

        self.helpmenu.add_command(label="sdtDBNs GUI webpage", command=self.gotoWebpage_GUI)
        self.helpmenu.add_command(label="sdtDBNs GUI Github project", command=self.gotoRepo_GUI)

        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        frame.config(menu=self.menubar)

    def gotoWebpage_sdtDBN(self):
        webbrowser.open_new('https://ttlion.github.io/sdtDBN/')
        return

    def gotoWebpage_GUI(self):
        webbrowser.open_new('https://ttlion.github.io/sdtDBN/')
        return
    
    def gotoRepo_sdtDBN(self):
        webbrowser.open_new('https://github.com/ttlion/sdtDBN_code')
        return
    
    def gotoRepo_GUI(self):
        webbrowser.open_new('https://github.com/ttlion/sdtDBNsGUI')
        return
    