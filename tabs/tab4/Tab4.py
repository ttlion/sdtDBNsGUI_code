from tkinter import *
from tkinter import scrolledtext

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

import csv
import subprocess
import os

class Tab4:

    def __init__(self, mainFrame, width):
        self.framePredictProgres = ttk.Frame(mainFrame, width=width)
        self.framePredictProgres.grid(row=1, column=1, rowspan=2)

        self.frameInfResults = ttk.Frame(self.framePredictProgres, width=width)
        self.frameInfResults.grid(row=1, column=3, rowspan=27)

        self.widthLeft = 30
        self.widthCenter = 15
        self.widthInput = 5

        # Create a Tkinter variable for available ids
        self.idTab4TkVar = StringVar(self.framePredictProgres)
        self.idTab4Choices = [ 'Inference observations not given!' ]

        self.idTab4 = ElemTwoSelect(self.framePredictProgres, "Desired id: ", self.widthLeft, self.idTab4TkVar, self.idTab4Choices, self.idTab4Choices[0], 1, 1 )

        # Create a Tkinter variable for available attributes
        self.attTab4TkVar = StringVar(self.framePredictProgres)
        self.attTab4Choices = [ 'There is not an sdtDBN learned!' ]

        self.attTab4 = ElemTwoSelect(self.framePredictProgres, "Desired attribute: ", self.widthLeft, self.attTab4TkVar, self.attTab4Choices, self.attTab4Choices[0], 2, 1 )

        # Create a Tkinter variable for timesteps
        self.timestepTab4 = ElemTwoInput(self.framePredictProgres, "Maximum timestep: ", self.widthLeft, self.widthInput, 3, 1, 1)

        # Create a Tkinter variable for the modes
        self.modeTab4TkVar = StringVar(self.framePredictProgres)
        self.modeTab4Choices = [ 'Distribution', 'Most Probable', 'Random Estimation using probability distributions' ]

        self.modeTab4 = ElemTwoSelect(self.framePredictProgres, "Desired estimation mode: ", self.widthLeft, self.modeTab4TkVar, self.modeTab4Choices, self.modeTab4Choices[0], 4, 1 )

        self.modesDict = {
            'Distribution' : 'distrib',
            'Most Probable' : 'mostProb',
            'Random Estimation using probability distributions' : 'distrSampl'
        }

        # Button to submit, making inference
        self.makeInfTab4 = ttk.Button(self.framePredictProgres, text = "Make inference", command = self.onSubmit)
        self.makeInfTab4.grid(row=5, column=1, columnspan=2, sticky = N+S+E+W)

    def changeAttOptions(self, newOptionsList):

        self.attTab4.destroy()

        self.attTab4Choices = ['all'] + newOptionsList

        self.attTab4 = ElemTwoSelect(self.framePredictProgres, "Desired attribute: ", 20, self.attTab4TkVar, self.attTab4Choices, self.attTab4Choices[0], 2, 1 )

    def changeIdsOptions(self, newOptionsList):

        self.idTab4.destroy()

        self.idTab4Choices = newOptionsList

        self.idTab4 = ElemTwoSelect(self.framePredictProgres, "Desired id: ", 20, self.idTab4TkVar, self.idTab4Choices, self.idTab4Choices[0], 1, 1 )

    def getInfSpecs(self, dynObsInfFilename, staticObsInfFilename):

        self.dynObsInfFilename = dynObsInfFilename
        self.staticObsInfFilename = staticObsInfFilename
        
        dynInfFile = open(self.dynObsInfFilename)
        reader = csv.reader(dynInfFile, delimiter=',')
        next(reader) # skip 1st line
        idList = []
        for row in reader:
            idList.append(row[0])
        dynInfFile.close()

        self.changeIdsOptions(idList)

        return
    
    def getLearningCmdArgs(self, learningCmdArgs):
        self.learningCmdArgs = learningCmdArgs
        return

    def onSubmit(self):
        desiredID = self.idTab4TkVar.get()

        auxDynInfFilename = 'auxDynInf.csv'
        auxStaticInfFilename = 'auxStaticInf.csv'
        auxInfVarFilename = 'auxInfVar.csv'

        dynInfFile = open(self.dynObsInfFilename)
        reader = csv.reader(dynInfFile, delimiter=',')
        firstLine = next(reader)
        desiredLineDyn = []
        for row in reader:
            if(row[0] == desiredID ):
                desiredLineDyn = row
                break
        dynInfFile.close()

        with open(auxDynInfFilename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(firstLine)
            writer.writerow(desiredLineDyn)

        staticInfFile = open(self.staticObsInfFilename)
        reader = csv.reader(staticInfFile, delimiter=',')
        firstLine = next(reader)
        desiredLineStatic = []
        for row in reader:
            if(row[0] == desiredID ):
                desiredLineStatic = row
                break
        staticInfFile.close()

        with open(auxStaticInfFilename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(firstLine)
            writer.writerow(desiredLineStatic)
        
        if(self.attTab4TkVar.get() != 'all'):
            desiredAtt = self.attTab4TkVar.get()
            maxTimestep = int(self.timestepTab4.entry.get())
            with open(auxInfVarFilename, 'w', newline='') as file:
                writer = csv.writer(file)
                i=0
                while (i<=maxTimestep):
                    infAttInList = [desiredAtt, i ]
                    writer.writerow(infAttInList)
                    i+=1
        else:
            maxTimestep = int(self.timestepTab4.entry.get())
            with open(auxInfVarFilename, 'w', newline='') as file:
                writer = csv.writer(file)
                for att in self.attTab4Choices:
                    if(att == 'all'):
                        continue
                    i=0
                    while (i<=maxTimestep):
                        infAttInList = [att, i]
                        writer.writerow(infAttInList)
                        i+=1


        infCmdArgs = ['-obs', auxDynInfFilename, '-obsStatic', auxStaticInfFilename, '-inf', auxInfVarFilename, '-infFmt', self.modesDict.get(self.modeTab4TkVar.get()) ]

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        p = subprocess.Popen(['java', '-jar', 'sdtDBN_v0_0_1.jar']  + self.learningCmdArgs + infCmdArgs , startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')
        
        self.infResult = p.stdout.read()

        p.terminate()
        os.remove(auxDynInfFilename)
        os.remove(auxStaticInfFilename)
        os.remove(auxInfVarFilename)

        for widget in self.frameInfResults.winfo_children():
             widget.destroy()

        textInfo = scrolledtext.ScrolledText(self.frameInfResults, height=27, width=45)
        textInfo.grid(row=1, column=4, rowspan=27, padx=7)
        textInfo.insert(END, self.infResult)

        return
