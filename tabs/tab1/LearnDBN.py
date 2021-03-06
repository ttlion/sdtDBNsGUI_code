from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk

import subprocess
import csv

from ..tab1.PageElements import *

from tabs.tab3 import *
from tabs.tab2 import *

class LearnDBN:

    def __init__(self, superFrame, message, row, column, pageElements, tab1_2, tab2, tab3, tab4, tab5):
        self.tab1_2 = tab1_2
        self.tab2 = tab2
        self.tab3 = tab3
        self.tab4 = tab4
        self.tab5 = tab5

        self.superFrame = superFrame
        self.row = row
        self.column = column
        self.message = message

        self.pageElements = pageElements

        self.submitButton = ttk.Button(superFrame, text = message, command=self.onSubmit)
        self.submitButton.grid(row=self.row, column=1, columnspan=3, sticky = N+S+E+W)
        
        self.submitionframe = ttk.Frame(superFrame)
        self.submitionframe.grid(row=self.row+1, column=self.column, columnspan=3)

        self.presentDBNFrame = ttk.Frame(superFrame)
        self.presentDBNFrame.grid(row=1, column=5, rowspan=10)

        self.presentDBNAttsFrame = ttk.Frame(superFrame)
        self.presentDBNAttsFrame.grid(row=1, column=4, rowspan=10)

        self.dynAttList = []
        self.staticAttList = []

        self.sfDict = {
            'Log-Likelihood (LL)' : 'll',
            'Minimum Description Length (MDL)' : 'mdl'
        }

        self.statDict = {
            'yes' : '',
            'no' : '-ns'
        }

        self.statDictBool = {
            'yes' : True,
            'no' : False
        }

    def onSubmit(self):
        for widget in self.submitionframe.winfo_children():
            widget.destroy()

        for widget in self.presentDBNAttsFrame.winfo_children():
            widget.destroy()

        for widget in self.presentDBNFrame.winfo_children():
            widget.destroy()

        printInfo = ttk.Label(self.submitionframe, text="Analyzing inputs", style="ok.TLabel")
        printInfo.grid(row=2, column=1, columnspan=3)

        dynObsFileName = self.pageElements.getElem("dynObs").FileName
        if(self.checkDynAtt(dynObsFileName) == False):
            return

        staticObsFileName = self.pageElements.getElem("staticObs").FileName

        self.hasStatic = self.checkstaticAtt(staticObsFileName)

        if ( self.checkEntryArgs() == False):
            return

        markovLag = self.pageElements.getElem("markovLag").entry.get()
        pValue = self.pageElements.getElem("pValue").entry.get()

        if(self.hasStatic == True):
            bValue = self.pageElements.getElem("bValue").entry.get()
        
        sfValue = self.sfDict.get(self.pageElements.getElem("sfValue").tkVar.get())
        stationaryValue = self.statDict.get(self.pageElements.getElem("stationaryValue").tkVar.get())
        self.isStationary = self.statDictBool.get(self.pageElements.getElem("stationaryValue").tkVar.get())

        self.fileToSave = self.pageElements.getElem("fileToSave").entry.get()

        if(self.checkFileToSave() == False):
            return

        self.restrictionsArgs = []
        if(self.checkRestrictions(self.hasStatic) == False):
            return

        printInfo = ttk.Label(self.submitionframe, text="All inputs in proper format, learning sdtDBN", style="ok.TLabel")
        printInfo.grid(row=10, column=1, columnspan=3)

        if(self.hasStatic == True):
            self.learningCmdArgs = ['-i', dynObsFileName, '-is', staticObsFileName, '-m', markovLag, '-p', pValue, '-b', bValue, '-s', sfValue, '-pm', stationaryValue, '-toFile', self.fileToSave] + self.restrictionsArgs
        else:
            self.learningCmdArgs = ['-i', dynObsFileName, '-m', markovLag, '-p', pValue, '-s', sfValue, '-pm', stationaryValue, '-toFile', self.fileToSave] + self.restrictionsArgs

        p = subprocess.run(['java', '-jar', 'sdtDBN_v0_0_1.jar'] + self.learningCmdArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')

        if(p.stderr != ''):
            self.learnedsdtDBN_text = p.stderr + p.stdout
            printInfo = ttk.Label(self.submitionframe, text="Problem with input arguments content: sdtDBN was NOT learned!", style="notok.TLabel")
            printInfo.grid(row=11, column=1, columnspan=3)
            self.presentOutputToUser()
            return

        self.learnedsdtDBN_text = p.stdout

        printInfo = ttk.Label(self.submitionframe, text="sdtDBN was learned!", style="ok.TLabel")
        printInfo.grid(row=11, column=1, columnspan=3)

        self.presentOutputToUser()
        self.giveArgsToOtherTabs()


    def checkDynAtt(self, dynObsFileName):

        if(dynObsFileName == "Not yet selected!" or dynObsFileName == ""):
            printInfo = ttk.Label(self.submitionframe, text="Dynamic observations file not given!", style="notok.TLabel")
            printInfo.grid(row=3, column=1, columnspan=3)
            return False

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

        return True

    def checkstaticAtt(self, staticObsFileName):
        if(staticObsFileName == "Not yet selected!" or staticObsFileName == ""):
            printInfo = ttk.Label(self.submitionframe, text="Static observations file not given!\nA DBN only with dynamic attributes will be learned!", style="ok.TLabel", justify='center')
            printInfo.grid(row=3, column=1, columnspan=3)
            return False
        
        staticAttFile = open(staticObsFileName)

        reader = csv.reader(staticAttFile, delimiter=',')

        firstLine = next(reader)

        self.staticAttList = []
        
        for element in firstLine[1:]:
            self.staticAttList.append(element)

        staticAttFile.close()

        return True
    
    def checkEntryArgs(self):
        
        if (self.hasStatic == True):
            errorMessagesDict = {
                'markovLag' : ['Markov lag must be > 0 !', 1],
                'pValue' : ['Number of parents from past must be > 0 !', 1],
                'bValue' : ['Number of static parents must be >= 0 !', 0]
            }
        else:
            errorMessagesDict = {
                'markovLag' : ['Markov lag must be > 0 !', 1],
                'pValue' : ['Number of parents from past must be > 0 !', 1]
            }

        for key, value in errorMessagesDict.items():
            if(self.is_integer(self.pageElements.getElem(key).entry.get()) == False):
                printInfo = ttk.Label(self.submitionframe, text = key + " is not an integer!", style="notok.TLabel")
                printInfo.grid(row=4, column=1, columnspan=3)
                return False

            number = int( self.pageElements.getElem(key).entry.get() )
            if(number < value[1] ):
                printInfo = ttk.Label(self.submitionframe, text=value[0], style="notok.TLabel")
                printInfo.grid(row=4, column=1, columnspan=3)
                return False

        return True

    def is_integer(self, value: str) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def checkFileToSave(self):
        if( self.fileToSave == '' ):
            printInfo = ttk.Label(self.submitionframe, text="File to save sdtDBN was not specified!", style="notok.TLabel")
            printInfo.grid(row=4, column=1, columnspan=3)
            return False
        return True

    def checkRestrictions(self, hasStatic):
        restrictionsDict = {
            "mA_dynPast" : "mandatory dynamic parents from previous timesteps",
            "mA_dynSame" : "mandatory dynamic parents from the same timestep",
            "mA_static" : "mandatory static parents",
            "mNotA_dynPast" : "forbidden dynamic parents from previous timesteps",
            "mNotA_dynSame" : "forbidden dynamic parents from the same timestep",
            "mNotA_static" : "forbidden static parents"
        }

        # Check all restrictions args and fill self.restrictionsArgs String accordingly
        i = 4
        for key, value in restrictionsDict.items():
            fileName = self.pageElements.getElem(key).FileName

            if(fileName == "Not yet selected!" or fileName == ""):
                continue
            
            if( (("static" in key) == True) and (hasStatic == False) ):
                printInfo = ttk.Label(self.submitionframe, text = "There were given restrictions on static parents but no static observations were given!", style="notok.TLabel")
                printInfo.grid(row=i, column=1, columnspan=3)
                return False

            self.restrictionsArgs += ["-" + key] + [fileName]

            printInfo = ttk.Label(self.submitionframe, text = "There were given " + value, style="ok.TLabel")    
            printInfo.grid(row=i, column=1, columnspan=3)
            i+=1

        return True

    def presentOutputToUser(self):
        self.presentAttsToUser()

        textInfo = scrolledtext.ScrolledText(self.presentDBNFrame, height=33, width=45)
        textInfo.grid(row=1, column=1, rowspan=33, padx=7)
        textInfo.insert(END, self.learnedsdtDBN_text)

    def presentAttsToUser(self):

        textInfo = scrolledtext.ScrolledText(self.presentDBNAttsFrame, height=33, width=15)
        textInfo.grid(row=1, column=1, rowspan=33, padx=7)
        textInfo.insert(END, "Dynamic Atts:\n")
        for element in self.dynAttList:
            textInfo.insert(END, element + "\n")

        if(self.hasStatic == True):
            textInfo.insert(END, "\nStatic Atts:\n")
            for element in self.staticAttList:
                textInfo.insert(END, element + "\n")

    def giveArgsToOtherTabs(self):

        self.tab1_2.setDBNFile(self.fileToSave)
        self.tab2.setDBNFile(self.fileToSave, self.hasStatic)
        self.tab3.setDBNFile(self.fileToSave)
        self.tab4.setDBNFile(self.fileToSave)
        self.tab5.setDBNFile(self.fileToSave)

        self.tab3.changeAttOptions(self.dynAttList)
        self.tab4.changeAttOptions(self.dynAttList)