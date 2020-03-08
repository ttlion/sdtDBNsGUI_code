from tkinter import *

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

import csv

class Tab4:

    def __init__(self, mainFrame, width):
        self.framePredictProgres = Frame(mainFrame, width=width)
        self.framePredictProgres.grid(row=1, column=1, rowspan=2)

        # Create a Tkinter variable for available ids
        self.idTab4TkVar = StringVar(self.framePredictProgres)
        self.idTab4Choices = [ 'Inference observations not given!' ]

        self.idTab4 = ElemTwoSelect(self.framePredictProgres, "Desired id: ", 20, self.idTab4TkVar, self.idTab4Choices, self.idTab4Choices[0], 1, 1 )

        # Create a Tkinter variable for available attributes
        self.attTab4TkVar = StringVar(self.framePredictProgres)
        self.attTab4Choices = [ 'There is not an sdtDBN learned!' ]

        self.attTab4 = ElemTwoSelect(self.framePredictProgres, "Desired attribute: ", 20, self.attTab4TkVar, self.attTab4Choices, self.attTab4Choices[0], 2, 1 )

        # Create a Tkinter variable for timesteps
        self.timestepTab4 = ElemTwoInput(self.framePredictProgres, "Maximum timestep: ", 20, 5, 3, 1)

        # Button to submit, making inference
        self.makeInfTab4 = Button(self.framePredictProgres, text = "Make inference", borderwidth = 10, width=20, command = self.onSubmit)
        self.makeInfTab4.grid(row=6, column=1, columnspan=2, sticky = N+S+E+W)

    def changeAttOptions(self, newOptionsList):

        self.attTab4.destroy()

        self.attTab4Choices = newOptionsList

        self.attTab4 = ElemTwoSelect(self.framePredictProgres, "Desired attribute: ", 20, self.attTab4TkVar, self.attTab4Choices, self.attTab4Choices[0], 2, 1 )

    def changeIdsOptions(self, newOptionsList):

        self.idTab4.destroy()

        self.idTab4Choices = newOptionsList

        self.idTab4 = ElemTwoSelect(self.framePredictProgres, "Desired id: ", 20, self.idTab4TkVar, self.idTab4Choices, self.idTab4Choices[0], 1, 1 )

    def getInfSpecs(self, dynObsInfFilename, staticObsInfFilename, estimationMode ):

        self.dynObsInfFilename = dynObsInfFilename
        self.staticObsInfFilename = staticObsInfFilename
        self.estimationMode = estimationMode
        
        dynInfFile = open(self.dynObsInfFilename)
        reader = csv.reader(dynInfFile, delimiter=',')
        next(reader) # skip 1st line
        idList = []
        for row in reader:
            idList.append(row[0])
        dynInfFile.close()

        self.changeIdsOptions(idList)

        return

    def onSubmit(self):
        return
