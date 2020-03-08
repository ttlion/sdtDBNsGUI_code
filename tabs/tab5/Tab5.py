from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import subprocess

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

class Tab5:

    def __init__(self, mainFrame, width):

        self.framePredictMany = Frame(mainFrame, width=width)
        self.framePredictMany.grid(row=1, column=1, rowspan=10)

        # Define desired mode
        self.desiredModeTab5TkVar = StringVar(self.framePredictMany)
        self.desiredModeTab5Choices = [ 'attribute inference', 'progression until timestep' ]

        self.desiredModeTab5 = ElemTwoSelect(self.framePredictMany, "Desired mode: ", 35, self.desiredModeTab5TkVar, 
                                                self.desiredModeTab5Choices, self.desiredModeTab5Choices[0], 1, 1 )

        # This is selected by default
        self.timestepOrVarsToInf_Tab5 = ElemThree(self.framePredictMany, 2, 1, "File with vars to inference: ", "Not yet selected!", 35)

        # When this var changes, it should be created the proper box
        self.desiredModeTab5TkVar.trace("w", self.createProperBox)

        # Create a Tkinter variable for output filename
        self.outputPathTab5 = ElemTwoInput(self.framePredictMany, "Output filename: ", 35, 15, 3, 1)

        # Button to submit, making inference
        self.makeInfTab5 = Button(self.framePredictMany, text = "Make inference", borderwidth = 10, width=35, command = self.onSubmit)
        self.makeInfTab5.grid(row=4, column=1, columnspan=3, sticky = N+S+E+W)


    def createProperBox(self, *args):

        self.timestepOrVarsToInf_Tab5.destroy()

        if(self.desiredModeTab5TkVar.get() == 'attribute inference' ):
            # Create variable to insert file with vars to inference
            self.timestepOrVarsToInf_Tab5 = ElemThree(self.framePredictMany, 2, 1, "File with vars to inference: ", "Not yet selected!", 35)
        else:
            # Create a Tkinter variable for timesteps
            self.timestepOrVarsToInf_Tab5 = ElemTwoInput(self.framePredictMany, "Maximum timestep: ", 35, 3, 2, 1)

    def onSubmit(self):
        return
