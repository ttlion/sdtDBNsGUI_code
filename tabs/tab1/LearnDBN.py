from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext

import subprocess

from ..tab1.PageElements import *

class LearnDBN:

    def __init__(self, superFrame, message, maxWidth, row, column, pageElements):
        self.superFrame = superFrame
        self.row = row
        self.column = column
        self.width = maxWidth
        self.message = message

        self.pageElements = pageElements
        
        self.submitionframe = Frame(superFrame, width=2000)
        self.submitionframe.grid(row=self.row, column=self.column, columnspan=3)

        self.submitButton = Button(self.submitionframe, text = message, borderwidth = 10, width=self.width, command=self.onSubmit)
        self.submitButton.grid(row=1, column=1, columnspan=3, sticky = N+S+E+W)

        self.presentDBNFrame = Frame(superFrame, width=50)
        self.presentDBNFrame.grid(row=1, column=5, rowspan=10)

    def onSubmit(self):
        for widget in self.submitionframe.winfo_children():
            widget.destroy()

        self.submitButton = Button(self.submitionframe, text = self.message, borderwidth = 10, width=self.width, command=self.onSubmit)
        self.submitButton.grid(row=1, column=1, columnspan=3, sticky = N+S+E+W)

        printInfo = Label(self.submitionframe, text="Analyzing inputs")
        printInfo.grid(row=2, column=1, columnspan=3)

        dynObsFileName = self.pageElements.getElem("dynObs").FileName
        if(dynObsFileName == "Not yet selected!"):
            printInfo = Label(self.submitionframe, text="Dynamic observations file not given!", fg="red")
            printInfo.grid(row=3, column=1, columnspan=3)
            return

        staticObsFileName = self.pageElements.getElem("staticObs").FileName
        if(staticObsFileName == "Not yet selected!"):
            printInfo = Label(self.submitionframe, text="Static observations file not given!", fg="red")
            printInfo.grid(row=3, column=1, columnspan=3)
            return
        
        markovLag = int( self.pageElements.getElem("markovLag").entry.get() )
        if(markovLag <= 0 ):
            printInfo = Label(self.submitionframe, text="Markov lag must be > 0 !", fg="red")
            printInfo.grid(row=3, column=1, columnspan=3)
            return
        
        pValue = int ( self.pageElements.getElem("pValue").entry.get() )
        if(pValue <= 0 ):
            printInfo = Label(self.submitionframe, text="Number of parents from past must be > 0 !", fg="red")
            printInfo.grid(row=3, column=1, columnspan=3)
            return
        
        bValue = int ( self.pageElements.getElem("bValue").entry.get() )
        if(bValue < 0 ):
            printInfo = Label(self.submitionframe, text="Number of static parents must be >= 0 !", fg="red")
            printInfo.grid(row=3, column=1, columnspan=3)
            return

        sfValue = self.pageElements.getElem("sfValue").tkVar.get()
        if(sfValue == "Log-Likelihood (LL)"):
            sfValue = "ll"
        else:
            sfValue = "mdl"

        stationaryValue = self.pageElements.getElem("stationaryValue").tkVar.get()
        if(stationaryValue == "yes"):
            stationaryValue = ""
        else:
            stationaryValue = "-ns"

        printInfo = Label(self.submitionframe, text="All inputs given, checking their format")
        printInfo.grid(row=3, column=1, columnspan=3)

        ## TODO: Check if all inputs in proper format

        printInfo = Label(self.submitionframe, text="All inputs in proper format, learning sdtDBN")
        printInfo.grid(row=4, column=1, columnspan=3)

        ## Call sdtDBN program and put output in txt file for future usage
        fileWithDBN = open("sdtDBN_output.txt", "w")

        subprocess.call(['java', '-jar', 'sdtDBN_v0_0_1.jar', '-i', dynObsFileName, '-is', staticObsFileName, '-m', str(markovLag), '-p', str(pValue), '-b', str(bValue), '-s', sfValue, '-pm', stationaryValue], stdout=fileWithDBN)

        fileWithDBN.close()

        printInfo = Label(self.submitionframe, text="sdtDBN was learned!")
        printInfo.grid(row=5, column=1, columnspan=3)

        for widget in self.presentDBNFrame.winfo_children():
            widget.destroy()

        fileWithDBN = open("sdtDBN_output.txt", "r")

        num_lines = sum(1 for line in fileWithDBN)
        fileWithDBN.seek(0)
        textInfo = scrolledtext.ScrolledText(self.presentDBNFrame, height=num_lines, width=45)
        textInfo.grid(row=1, column=1, rowspan=num_lines, padx=7)
        textInfo.insert(END, fileWithDBN.read())


        fileWithDBN.close()

