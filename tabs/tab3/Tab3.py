from tkinter import *

from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

class Tab3:

    def __init__(self, mainFrame, width):
        self.framePredictSpecific = Frame(mainFrame, width=width)
        self.framePredictSpecific.grid(row=1, column=1, rowspan=2)

        # Create a Tkinter variable for available ids
        self.idTab3TkVar = StringVar(self.framePredictSpecific)
        self.idTab3Choices = [ '1', '2', '3' ]

        self.idTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired id: ", 20, self.idTab3TkVar, self.idTab3Choices, self.idTab3Choices[0], 1, 1 )

        # Create a Tkinter variable for available attributes
        self.attTab3TkVar = StringVar(self.framePredictSpecific)
        self.attTab3Choices = [ 'a', 'b', 'c' ]

        self.attTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired attribute: ", 20, self.attTab3TkVar, self.attTab3Choices, self.attTab3Choices[0], 2, 1 )

        # Create a Tkinter variable for timesteps
        self.timestepTab3 = ElemTwoInput(self.framePredictSpecific, "Desired timestep: ", 20, 5, 3, 1)

        self.makeInfTab3 = Button(self.framePredictSpecific, text = "Make inference", borderwidth = 10, width=20, command = self.onSubmit)
        self.makeInfTab3.grid(row=6, column=1, columnspan=2, sticky = N+S+E+W)

    def onSubmit(self):
        return
