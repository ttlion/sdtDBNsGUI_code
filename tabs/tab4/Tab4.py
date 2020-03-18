from tkinter import *
from tkinter import scrolledtext

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *
from utils.ElemTwoPresent import *

import csv
import subprocess
import os

class Tab4:

    def __init__(self, mainFrame, width):
        self.framePredictProgres = ttk.Frame(mainFrame, width=width)
        self.framePredictProgres.grid(row=1, column=1, rowspan=2)

        self.frameInfResults = ttk.Frame(self.framePredictProgres, width=width)
        self.frameInfResults.grid(row=1, column=3, rowspan=27)

        self.frameErrors = ttk.Frame(self.framePredictProgres, width=width)
        self.frameErrors.grid(row=7, column=1, rowspan=3)

        self.widthLeft = 30
        self.widthCenter = 15
        self.widthInput = 5

        self.staticObsGiven = False # By default put as not having static observations

        # Present filename of DBN being used
        self.showDBN = ElemTwoPresent(self.framePredictProgres, "sdtDBN being used: ", "No file yet selected", self.widthLeft, 1, 1)

        # Create a Tkinter variable for available ids
        self.idTab4TkVar = StringVar(self.framePredictProgres)
        self.idTab4Choices = [ 'Inference observations not given!' ]

        self.idTab4 = ElemTwoSelect(self.framePredictProgres, "Desired id: ", self.widthLeft, self.idTab4TkVar, self.idTab4Choices, self.idTab4Choices[0], 2, 1 )

        # Create a Tkinter variable for available attributes
        self.attTab4TkVar = StringVar(self.framePredictProgres)
        self.attTab4Choices = [ 'There is not an sdtDBN learned!' ]

        self.attTab4 = ElemTwoSelect(self.framePredictProgres, "Desired attribute: ", self.widthLeft, self.attTab4TkVar, self.attTab4Choices, self.attTab4Choices[0], 3, 1 )

        # Create a Tkinter variable for timesteps
        self.timestepTab4 = ElemTwoInput(self.framePredictProgres, "Maximum timestep: ", self.widthLeft, self.widthInput, 4, 1, 1)

        # Create a Tkinter variable for the modes
        self.modeTab4TkVar = StringVar(self.framePredictProgres)
        self.modeTab4Choices = [ 'Distribution', 'Most Probable', 'Random Estimation using probability distributions' ]

        self.modeTab4 = ElemTwoSelect(self.framePredictProgres, "Desired estimation mode: ", self.widthLeft, self.modeTab4TkVar, self.modeTab4Choices, self.modeTab4Choices[0], 5, 1 )

        self.modesDict = {
            'Distribution' : 'distrib',
            'Most Probable' : 'mostProb',
            'Random Estimation using probability distributions' : 'distrSampl'
        }

        # Button to submit, making inference
        self.makeInfTab4 = ttk.Button(self.framePredictProgres, text = "Make inference", command = self.onSubmit)
        self.makeInfTab4.grid(row=6, column=1, columnspan=2, sticky = N+S+E+W)

    def changeAttOptions(self, newOptionsList):

        self.attTab4.destroy()

        self.attTab4Choices = ['all'] + newOptionsList

        self.attTab4 = ElemTwoSelect(self.framePredictProgres, "Desired attribute: ", self.widthLeft, self.attTab4TkVar, self.attTab4Choices, self.attTab4Choices[0], 3, 1 )

    def changeIdsOptions(self, newOptionsList):

        self.idTab4.destroy()

        self.idTab4Choices = newOptionsList

        self.idTab4 = ElemTwoSelect(self.framePredictProgres, "Desired id: ", self.widthLeft, self.idTab4TkVar, self.idTab4Choices, self.idTab4Choices[0], 2, 1 )

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

        if(staticObsInfFilename == "Not yet selected!" or staticObsInfFilename == ''):
            self.staticObsGiven = False
        else:
            self.staticObsGiven = True

        return

    def onSubmit(self):

        if(self.checkArgs() == False):
            return

        desiredID = self.idTab4TkVar.get()

        auxDynInfFilename = 'auxDynInf.csv'
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

        if(self.staticObsGiven == True):
            auxStaticInfFilename = 'auxStaticInf.csv'
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

        if(self.modeTab4TkVar.get() == 'Distribution'):
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

        infCmdArgs = ['-obs', auxDynInfFilename, '-infFmt', self.modesDict.get(self.modeTab4TkVar.get())]

        if(self.staticObsGiven == True):
            infCmdArgs = infCmdArgs + ['-obsStatic', auxStaticInfFilename]

        if(self.modeTab4TkVar.get() == 'Distribution'):
            infCmdArgs = infCmdArgs + ['-inf', auxInfVarFilename]
        else:
            infCmdArgs = infCmdArgs + ['-t', self.timestepTab4.entry.get()]
            if(self.attTab4TkVar.get() != 'all'):
                infCmdArgs = infCmdArgs + ['-tf', 'auxFile.csv']

        p = subprocess.run(['java', '-jar', 'sdtDBN_v0_0_1.jar', '-fromFile', self.showDBN.messageRight] + infCmdArgs , stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')
        
        self.infResult = p.stdout

        if(self.modeTab4TkVar.get() != 'Distribution' and self.attTab4TkVar.get() != 'all'):
            
            attToKeep = self.attTab4TkVar.get()
            with open('auxFile.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)

                header = [reader.fieldnames[0]]
                for elem in reader.fieldnames:
                    if (attToKeep == elem.split('__')[0]):
                        header = header + [ elem ]
                string = ','.join(header)
                
                for row in reader:
                    newLine = [ row[header[0]] ]
                    for key in row:
                        if (attToKeep == key.split('__')[0]):
                            newLine = newLine + [ row[key] ]
                    string = string + "\n" + (','.join(newLine))

            self.infResult = self.infResult + string
            os.remove('auxFile.csv')

        os.remove(auxDynInfFilename)
        
        if(self.modeTab4TkVar.get() == 'Distribution'):
            os.remove(auxInfVarFilename)
            
        if(self.staticObsGiven == True):
            os.remove(auxStaticInfFilename)

        for widget in self.frameInfResults.winfo_children():
             widget.destroy()

        textInfo = scrolledtext.ScrolledText(self.frameInfResults, height=27, width=45)
        textInfo.grid(row=1, column=4, rowspan=27, padx=7)
        textInfo.insert(END, self.infResult)

        return

    def checkArgs(self):
        for widget in self.frameErrors.winfo_children():
            widget.destroy()

        if (self.showDBN.messageRight == "No file yet selected" ):
            printInfo = ttk.Label(self.frameErrors, text="No DBN was selected!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False
        
        if(self.idTab4TkVar.get() == 'Inference observations not given!'):
            printInfo = ttk.Label(self.frameErrors, text="Inference observations not given!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False

        if(self.attTab4TkVar.get() == 'There is not an sdtDBN learned!'):
            printInfo = ttk.Label(self.frameErrors, text="No attribute was specified!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False
        
        if(self.is_integer(self.timestepTab4.entry.get()) == False):
            printInfo = ttk.Label(self.frameErrors, text = "Timestep is not an integer!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False

        if(int(self.timestepTab4.entry.get()) < 1):
            printInfo = ttk.Label(self.frameErrors, text = "Timestep must be > 0", style="notok.TLabel")
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
        self.showDBN = ElemTwoPresent(self.framePredictProgres, "sdtDBN being used: ", dbnFilename, self.widthLeft, 1, 1)
        return