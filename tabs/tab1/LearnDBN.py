from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext

import subprocess
import csv

from ..tab1.PageElements import *

from tabs.tab3 import *

class LearnDBN:

    def __init__(self, superFrame, message, maxWidth, row, column, pageElements, tab3, tab4, tab5):
        self.tab3 = tab3
        self.tab4 = tab4
        self.tab5 = tab5

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

        self.presentDBNAttsFrame = Frame(superFrame, width=50)
        self.presentDBNAttsFrame.grid(row=1, column=4, rowspan=10)

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

        self.checkDynAtt(dynObsFileName)

        self.tab3.changeAttOptions(self.dynAttList)
        self.tab4.changeAttOptions(self.dynAttList)
        self.tab5.changeAttributes(self.dynAttList)

        staticObsFileName = self.pageElements.getElem("staticObs").FileName
        if(staticObsFileName == "Not yet selected!"):
            printInfo = Label(self.submitionframe, text="Static observations file not given!", fg="red")
            printInfo.grid(row=3, column=1, columnspan=3)
            return
        
        self.checkstaticAtt(staticObsFileName)

        for widget in self.presentDBNAttsFrame.winfo_children():
            widget.destroy()

        textInfo = scrolledtext.ScrolledText(self.presentDBNAttsFrame, height=27, width=15)
        textInfo.grid(row=1, column=1, rowspan=27, padx=7)
        textInfo.insert(END, "Dynamic Atts:\n")
        for element in self.dynAttList:
            textInfo.insert(END, element + "\n")

        textInfo.insert(END, "\nStatic Atts:\n")
        for element in self.staticAttList:
            textInfo.insert(END, element + "\n")

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

        self.learningCmdArgs = ['-i', dynObsFileName, '-is', staticObsFileName, '-m', str(markovLag), '-p', str(pValue), '-b', str(bValue), '-s', sfValue, '-pm', stationaryValue]

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        p = subprocess.Popen(['java', '-jar', 'sdtDBN_v0_0_1.jar'] + self.learningCmdArgs, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')

        self.learnedsdtDBN_text = p.stdout.read()

        p.terminate()

        printInfo = Label(self.submitionframe, text="sdtDBN was learned!")
        printInfo.grid(row=5, column=1, columnspan=3)

        for widget in self.presentDBNFrame.winfo_children():
            widget.destroy()

        textInfo = scrolledtext.ScrolledText(self.presentDBNFrame, height=27, width=45)
        textInfo.grid(row=1, column=1, rowspan=27, padx=7)
        textInfo.insert(END, self.learnedsdtDBN_text)

        self.tab3.getLearningCmdArgs(self.learningCmdArgs)
        self.tab4.getLearningCmdArgs(self.learningCmdArgs)
        self.tab5.getLearningCmdArgs(self.learningCmdArgs)

    def checkDynAtt(self, dynObsFileName):

        dynAttFile = open(dynObsFileName)

        reader = csv.reader(dynAttFile, delimiter=',')

        firstLine = next(reader)

        self.dynAttList = []
        
        for element in firstLine[1:]:
            if(element.find('__0') == -1):
                break
            else:
                self.dynAttList.append( element.split('__0')[0] )

        dynAttFile.close()

        return

    def checkstaticAtt(self, staticObsFileName):
        
        staticAttFile = open(staticObsFileName)

        reader = csv.reader(staticAttFile, delimiter=',')

        firstLine = next(reader)

        self.staticAttList = []
        
        for element in firstLine[1:]:
            self.staticAttList.append(element)

        staticAttFile.close()

        return
