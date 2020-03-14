from tkinter import *
from tkinter import ttk
from graphviz import Source

from utils.ElemTwoInput import *
from utils.ElemTwoPresent import *

import subprocess

class Tab1_2:

    def __init__(self, mainFrame, width):

        self.frameInfoToImg = ttk.Frame(mainFrame, width=width)
        self.frameInfoToImg.grid(row=1, column=1, rowspan=10)

        self.frameErrors = ttk.Frame(self.frameInfoToImg, width=width)
        self.frameErrors.grid(row=4, column=1, columnspan=2)

        self.framePresentImg = ttk.Frame(self.frameInfoToImg, width=width)
        self.framePresentImg.grid(row=1, column=3, rowspan=40)

        self.widthLeft = 30
        self.widthCenter = 15
        self.widthInput = 25

        # Present filename of DBN being used
        self.showDBN = ElemTwoInputPresent(self.frameInfoToImg, "sdtDBN being used: ", "No file yet selected", self.widthLeft,self.widthCenter, 1, 1)

        # Create a Tkinter variable for output filename
        self.outputPathImg = ElemTwoInput(self.frameInfoToImg, "Image filename: ", self.widthLeft, self.widthInput, 2, 1, 'imgNameExample.png')

        # Button to submit, making inference
        self.makeInfTab5 = ttk.Button(self.frameInfoToImg, text = "Create Image", command = self.onSubmit)
        self.makeInfTab5.grid(row=3, column=1, columnspan=2, sticky = N+S+E+W)

    def onSubmit(self):

        for widget in self.frameErrors.winfo_children():
            widget.destroy()

        for widget in self.framePresentImg.winfo_children():
            widget.destroy()

        if( self.checkArgs() == False ):
            return

        p = subprocess.run(['java', '-jar', 'sdtDBN_v0_0_1.jar', '-fromFile', self.showDBN.messageRight, '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')

        dotSourceCode = p.stdout
        
        imgFileName = self.outputPathImg.entry.get()

        s = Source(dotSourceCode)
        
        s.render(filename = imgFileName, cleanup = True, format = 'png')

        self.img = PhotoImage(file = imgFileName + '.png')
        
        labelToPresentImg = ttk.Label(self.framePresentImg, image = self.img)
        labelToPresentImg.grid(row=1, column=1, rowspan=40)

        printInfo = ttk.Label(self.frameErrors, text="Image " + imgFileName + ".png was saved", style="ok.TLabel")
        printInfo.grid(row=1, column=1, columnspan=2)

        return

    def checkArgs(self):
        if(self.showDBN.messageRight == "No file yet selected" ):
            printInfo = ttk.Label(self.frameErrors, text="no sdtDBN file was given!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False
        if(self.outputPathImg.entry.get() == ''):
            printInfo = ttk.Label(self.frameErrors, text="An image filename must be specified!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False
        return True
    
    def setDBNFile(self, dbnFilename):
        self.showDBN.destroy()
        self.showDBN = ElemTwoInputPresent(self.frameInfoToImg, "sdtDBN being used: ", dbnFilename, self.widthLeft, self.widthCenter, 1, 1)
        return
