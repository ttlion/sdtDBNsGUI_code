from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
import subprocess

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *
from utils.ElemTwoPresent import *

class Tab5:

    def __init__(self, mainFrame, width):

        self.framePredictMany = ttk.Frame(mainFrame, width=width)
        self.framePredictMany.grid(row=1, column=1, rowspan=10)

        self.frameErrors = ttk.Frame(self.framePredictMany, width=width)
        self.frameErrors.grid(row=7, column=1, rowspan=3)

        self.frameInfResults = ttk.Frame(self.framePredictMany, width=width)
        self.frameInfResults.grid(row=1, column=4, rowspan=27)

        self.dynObsInfFilename = ''
        self.staticObsInfFilename = ''

        self.widthLeft = 30
        self.widthCenter = 15
        self.widthInput = 4

        self.staticObsGiven = False # By default put as not having static observations

        # Present filename of DBN being used
        self.showDBN = ElemTwoPresent(self.framePredictMany, "sdtDBN being used: ", "No file yet selected", self.widthLeft, 1, 1)

        # Define desired mode
        self.desiredModeTab5TkVar = StringVar(self.framePredictMany)
        self.desiredModeTab5Choices = [ 'Attribute inference', 'Progression until timestep' ]

        self.desiredModeTab5 = ElemTwoSelect(self.framePredictMany, "Desired mode: ", self.widthLeft, self.desiredModeTab5TkVar, 
                                                self.desiredModeTab5Choices, self.desiredModeTab5Choices[0], 2, 1 )

        self.onlyCSVfiles = [("csv files", "*.csv" )]

        # This is selected by default
        self.timestepOrVarsToInf_Tab5 = ElemThree(self.framePredictMany, 4, 1, "File with vars to inference: ", "Not yet selected!", self.widthLeft, self.widthCenter, self.onlyCSVfiles)

        # When this var changes, it should be created the proper box
        self.desiredModeTab5TkVar.trace("w", self.createProperBox)

        # Create a Tkinter variable for the modes
        self.estimModeTab5TkVar = StringVar(self.framePredictMany)
        self.estimModeTab5Choices = [ 'Distribution', 'Most Probable', 'Random Estimation using probability distributions' ]

        # By default, Distribution is presented also because it is presented att inference as the mode
        self.estimModeTab5 = ElemTwoSelect(self.framePredictMany, "Desired estimation mode: ", self.widthLeft, self.estimModeTab5TkVar, self.estimModeTab5Choices, self.estimModeTab5Choices[0], 3, 1 )

        self.estimModesDict = {
            'Distribution' : 'distrib',
            'Most Probable' : 'mostProb',
            'Random Estimation using probability distributions' : 'distrSampl'
        }

        # Create a Tkinter variable for output filename
        self.outputPathTab5 = ElemTwoInput(self.framePredictMany, "Output filename: ", self.widthLeft, 25, 5, 1, 'exampleOut.csv')

        # Button to submit, making inference
        self.makeInfTab5 = ttk.Button(self.framePredictMany, text = "Make inference", command = self.onSubmit)
        self.makeInfTab5.grid(row=6, column=1, columnspan=3, sticky = N+S+E+W)


    def createProperBox(self, *args):

        self.timestepOrVarsToInf_Tab5.destroy()
        self.estimModeTab5.destroy()

        if(self.desiredModeTab5TkVar.get() == 'Attribute inference' ):
            # Create variable to insert file with vars to inference
            self.timestepOrVarsToInf_Tab5 = ElemThree(self.framePredictMany, 4, 1, "File with vars to inference: ", "Not yet selected!", self.widthLeft, self.widthCenter, self.onlyCSVfiles)

            self.estimModeTab5Choices = [ 'Distribution', 'Most Probable', 'Random Estimation using probability distributions' ]

        else:
            # Create a Tkinter variable for timesteps
            self.timestepOrVarsToInf_Tab5 = ElemTwoInput(self.framePredictMany, "Maximum timestep: ", self.widthLeft, self.widthInput, 4, 1, 1)

            self.estimModeTab5Choices = [ 'Most Probable', 'Random Estimation using probability distributions' ]

        # Create estimModeTab5 with proper Choices
        self.estimModeTab5 = ElemTwoSelect(self.framePredictMany, "Desired estimation mode: ", self.widthLeft, self.estimModeTab5TkVar, self.estimModeTab5Choices, self.estimModeTab5Choices[0], 3, 1 )

        return

    def getInfSpecs(self, dynObsInfFilename, staticObsInfFilename):
        self.dynObsInfFilename = dynObsInfFilename
        self.staticObsInfFilename = staticObsInfFilename

        if(staticObsInfFilename == "Not yet selected!" or staticObsInfFilename == ''):
            self.staticObsGiven = False
        else:
            self.staticObsGiven = True

        return

    def onSubmit(self):
        
        if(self.checkArgs() == False):
            return

        infCmdArgs = ['-obs', self.dynObsInfFilename, '-infFmt', self.estimModesDict.get(self.estimModeTab5TkVar.get())]

        if(self.staticObsGiven == True):
            infCmdArgs = infCmdArgs + ['-obsStatic', self.staticObsInfFilename]

        if (self.desiredModeTab5TkVar.get() == 'Attribute inference' ):
            infCmdArgs = infCmdArgs + [ '-inf', self.timestepOrVarsToInf_Tab5.FileName , '-outInf', self.outputPathTab5.entry.get() ]
        else:
            infCmdArgs = infCmdArgs + ['-t', self.timestepOrVarsToInf_Tab5.entry.get() , '-tf', self.outputPathTab5.entry.get() ]

        p = subprocess.run(['java', '-jar', 'sdtDBN_v0_0_1.jar', '-fromFile', self.showDBN.messageRight ]  + infCmdArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')

        p.stdout

        printInfo = ttk.Label(self.frameErrors, text = "Desired prediction is also in the defined output file!", style="ok.TLabel")
        printInfo.grid(row=1, column=1, columnspan=2)

        with open(self.outputPathTab5.entry.get(), 'r') as file:
            outputFileData = file.read()
            textInfo = scrolledtext.ScrolledText(self.frameInfResults, height=33, width=45)
            textInfo.grid(row=1, column=1, rowspan=33, padx=7)
            textInfo.insert(END, outputFileData)

        return

    def checkArgs(self):
        for widget in self.frameErrors.winfo_children():
            widget.destroy()

        for widget in self.frameInfResults.winfo_children():
             widget.destroy()
        
        if (self.showDBN.messageRight == "No file yet selected" ):
            printInfo = ttk.Label(self.frameErrors, text="No DBN was selected!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False
        
        if(self.dynObsInfFilename == '' ):
            printInfo = ttk.Label(self.frameErrors, text="No file with dynamic observations was given!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False
        
        if(self.desiredModeTab5TkVar.get() == 'Attribute inference'):
            if(self.timestepOrVarsToInf_Tab5.FileName == "Not yet selected!" or self.timestepOrVarsToInf_Tab5.FileName == '' ):
                printInfo = ttk.Label(self.frameErrors, text="No file with variables to inference was given", style="notok.TLabel")
                printInfo.grid(row=1, column=1, columnspan=3)
                return False
        else:
            if(self.is_integer(self.timestepOrVarsToInf_Tab5.entry.get()) == False):
                printInfo = ttk.Label(self.frameErrors, text = "Maximum timestep is not an integer!", style="notok.TLabel")
                printInfo.grid(row=1, column=1, columnspan=2)
                return False

            if(int(self.timestepOrVarsToInf_Tab5.entry.get()) < 1):
                printInfo = ttk.Label(self.frameErrors, text = "Maximum timestep must be > 0", style="notok.TLabel")
                printInfo.grid(row=1, column=1, columnspan=2)
                return False
        
        if(self.outputPathTab5.entry.get() == ''):
            printInfo = ttk.Label(self.frameErrors, text = "Output filename not given!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False

        return True

    def is_integer(self, value: str) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def setDBNFile(self, dbnFilename):
        self.showDBN.destroy()
        self.showDBN = ElemTwoPresent(self.framePredictMany, "sdtDBN being used: ", dbnFilename, self.widthLeft, 1, 1)
        return