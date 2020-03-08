from tkinter import *

from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

import csv

class Tab3:

    def __init__(self, mainFrame, width):
        self.framePredictSpecific = Frame(mainFrame, width=width)
        self.framePredictSpecific.grid(row=1, column=1, rowspan=2)

        # Create a Tkinter variable for available ids
        self.idTab3TkVar = StringVar(self.framePredictSpecific)
        self.idTab3Choices = [ 'Inference observations not given!' ]

        self.idTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired id: ", 20, self.idTab3TkVar, self.idTab3Choices, self.idTab3Choices[0], 1, 1 )

        # Create a Tkinter variable for available attributes
        self.attTab3TkVar = StringVar(self.framePredictSpecific)
        self.attTab3Choices = [ 'There is not an sdtDBN learned!' ]

        self.attTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired attribute: ", 20, self.attTab3TkVar, self.attTab3Choices, self.attTab3Choices[0], 2, 1 )

        # Create a Tkinter variable for timesteps
        self.timestepTab3 = ElemTwoInput(self.framePredictSpecific, "Desired timestep: ", 20, 5, 3, 1)

        self.makeInfTab3 = Button(self.framePredictSpecific, text = "Make inference", borderwidth = 10, width=20, command = self.onSubmit)
        self.makeInfTab3.grid(row=6, column=1, columnspan=2, sticky = N+S+E+W)

    def onSubmit(self):
        return

    def changeAttOptions(self, newOptionsList):

        self.attTab3.destroy()

        self.attTab3Choices = newOptionsList

        self.attTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired attribute: ", 20, self.attTab3TkVar, self.attTab3Choices, self.attTab3Choices[0], 2, 1 )

    def changeIdsOptions(self, newOptionsList):

        self.idTab3.destroy()

        self.idTab3Choices = newOptionsList

        self.idTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired id: ", 20, self.idTab3TkVar, self.idTab3Choices, self.idTab3Choices[0], 1, 1 )

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

        print(idList)

        return