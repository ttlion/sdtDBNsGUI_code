from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import subprocess

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

class Tab5:

    def __init__(self, mainFrame, width):

        self.framePredictMany = ttk.Frame(mainFrame, width=width)
        self.framePredictMany.grid(row=1, column=1, rowspan=10)

        self.widthLeft = 30
        self.widthCenter = 15
        self.widthInput = 4

        # Define desired mode
        self.desiredModeTab5TkVar = StringVar(self.framePredictMany)
        self.desiredModeTab5Choices = [ 'Attribute inference', 'Progression until timestep' ]

        self.desiredModeTab5 = ElemTwoSelect(self.framePredictMany, "Desired mode: ", self.widthLeft, self.desiredModeTab5TkVar, 
                                                self.desiredModeTab5Choices, self.desiredModeTab5Choices[0], 1, 1 )

        # This is selected by default
        self.timestepOrVarsToInf_Tab5 = ElemThree(self.framePredictMany, 3, 1, "File with vars to inference: ", "Not yet selected!", self.widthLeft, self.widthCenter)

        # When this var changes, it should be created the proper box
        self.desiredModeTab5TkVar.trace("w", self.createProperBox)

        # Create a Tkinter variable for the modes
        self.estimModeTab5TkVar = StringVar(self.framePredictMany)
        self.estimModeTab5Choices = [ 'Distribution', 'Most Probable', 'Random Estimation using probability distributions' ]

        # By default, Distribution is presented also because it is presented att inference as the mode
        self.estimModeTab5 = ElemTwoSelect(self.framePredictMany, "Desired estimation mode: ", self.widthLeft, self.estimModeTab5TkVar, self.estimModeTab5Choices, self.estimModeTab5Choices[0], 2, 1 )

        self.estimModesDict = {
            'Distribution' : 'distrib',
            'Most Probable' : 'mostProb',
            'Random Estimation using probability distributions' : 'distrSampl'
        }

        # Create a Tkinter variable for output filename
        self.outputPathTab5 = ElemTwoInput(self.framePredictMany, "Output filename: ", self.widthLeft, 25, 4, 1, 'exampleOut.csv')

        # Button to submit, making inference
        self.makeInfTab5 = ttk.Button(self.framePredictMany, text = "Make inference", command = self.onSubmit)
        self.makeInfTab5.grid(row=5, column=1, columnspan=3, sticky = N+S+E+W)


    def createProperBox(self, *args):

        self.timestepOrVarsToInf_Tab5.destroy()
        self.estimModeTab5.destroy()

        if(self.desiredModeTab5TkVar.get() == 'Attribute inference' ):
            # Create variable to insert file with vars to inference
            self.timestepOrVarsToInf_Tab5 = ElemThree(self.framePredictMany, 3, 1, "File with vars to inference: ", "Not yet selected!", self.widthLeft, self.widthCenter)

            self.estimModeTab5Choices = [ 'Distribution', 'Most Probable', 'Random Estimation using probability distributions' ]

        else:
            # Create a Tkinter variable for timesteps
            self.timestepOrVarsToInf_Tab5 = ElemTwoInput(self.framePredictMany, "Maximum timestep: ", self.widthLeft, self.widthInput, 3, 1, 1)

            self.estimModeTab5Choices = [ 'Most Probable', 'Random Estimation using probability distributions' ]

        # Create estimModeTab5 with proper Choices
        self.estimModeTab5 = ElemTwoSelect(self.framePredictMany, "Desired estimation mode: ", self.widthLeft, self.estimModeTab5TkVar, self.estimModeTab5Choices, self.estimModeTab5Choices[0], 2, 1 )

        return

    def changeAttributes(self, dynAttList):
        self.dynAttList = dynAttList

    def getLearningCmdArgs(self, learningCmdArgs):
        self.learningCmdArgs = learningCmdArgs
        return

    def getInfSpecs(self, dynObsInfFilename, staticObsInfFilename):
        self.dynObsInfFilename = dynObsInfFilename
        self.staticObsInfFilename = staticObsInfFilename
        return

    def onSubmit(self):
        if (self.desiredModeTab5TkVar.get() == 'Attribute inference' ):
            infCmdArgs = ['-obs', self.dynObsInfFilename , '-obsStatic', self.staticObsInfFilename , '-inf', self.timestepOrVarsToInf_Tab5.FileName , '-infFmt', self.estimModesDict.get(self.estimModeTab5TkVar.get()), '-outInf', self.outputPathTab5.entry.get() ]

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            p = subprocess.Popen(['java', '-jar', 'sdtDBN_v0_0_1.jar']  + self.learningCmdArgs + infCmdArgs , startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')

            p.stdout.read()

            p.terminate()
        else:
            infCmdArgs = ['-obs', self.dynObsInfFilename , '-obsStatic', self.staticObsInfFilename , '-infFmt', self.estimModesDict.get(self.estimModeTab5TkVar.get()), '-t', self.timestepOrVarsToInf_Tab5.entry.get() , '-tf', self.outputPathTab5.entry.get() ]

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            p = subprocess.Popen(['java', '-jar', 'sdtDBN_v0_0_1.jar']  + self.learningCmdArgs + infCmdArgs , startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')

            p.stdout.read()

            p.terminate()

        return
