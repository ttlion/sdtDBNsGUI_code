from tkinter import *
from tkinter import scrolledtext

from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *
from utils.ElemTwoPresent import *

import subprocess
import csv
import os

class Tab3:

    def __init__(self, mainFrame, width):
        self.framePredictSpecific = ttk.Frame(mainFrame, width=width)
        self.framePredictSpecific.grid(row=1, column=1, rowspan=5)

        self.frameInfResults = ttk.Frame(self.framePredictSpecific, width=width)
        self.frameInfResults.grid(row=1, column=3, rowspan=27)

        self.frameErrors = ttk.Frame(self.framePredictSpecific, width=width)
        self.frameErrors.grid(row=6, column=1, rowspan=3)

        self.widthLeft = 30
        self.widthCenter = 15
        self.widthInput = 4

        self.staticObsGiven = False # By default put as not having static observations

        # Present filename of DBN being used
        self.showDBN = ElemTwoInputPresent(self.framePredictSpecific, "sdtDBN being used: ", "No file yet selected", self.widthLeft,self.widthCenter, 1, 1)

        # Create a Tkinter variable for available ids
        self.idTab3TkVar = StringVar(self.framePredictSpecific)
        self.idTab3Choices = [ 'Inference observations not given!' ]

        self.idTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired id: ", self.widthLeft, self.idTab3TkVar, self.idTab3Choices, self.idTab3Choices[0], 2, 1 )

        # Create a Tkinter variable for available attributes
        self.attTab3TkVar = StringVar(self.framePredictSpecific)
        self.attTab3Choices = [ 'There is not an sdtDBN learned!' ]

        self.attTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired attribute: ", self.widthLeft, self.attTab3TkVar, self.attTab3Choices, self.attTab3Choices[0], 3, 1 )

        # Create a Tkinter variable for timesteps
        self.timestepTab3 = ElemTwoInput(self.framePredictSpecific, "Desired timestep: ", self.widthLeft, self.widthInput, 4, 1, 1)

        self.makeInfTab3 = ttk.Button(self.framePredictSpecific, text = "Make inference", command = self.onSubmit)
        self.makeInfTab3.grid(row=5, column=1, columnspan=2, sticky = N+S+E+W)

    def onSubmit(self):

        if(self.checkArgs() == False):
            return
        
        desiredID = self.idTab3TkVar.get()

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
        
        infAttInList = [self.attTab3TkVar.get(), self.timestepTab3.entry.get() ]

        with open(auxInfVarFilename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(infAttInList)

        if(self.staticObsGiven == True):
            infCmdArgs = ['-obs', auxDynInfFilename, '-obsStatic', auxStaticInfFilename, '-inf', auxInfVarFilename, '-infFmt', 'distrib' ]
        else:
            infCmdArgs = ['-obs', auxDynInfFilename, '-inf', auxInfVarFilename, '-infFmt', 'distrib' ]

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        p = subprocess.Popen(['java', '-jar', 'sdtDBN_v0_0_1.jar', '-fromFile', self.showDBN.messageRight ] + infCmdArgs , startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')
        
        self.infResult = p.stdout.read()

        p.terminate()
        os.remove(auxDynInfFilename)
        os.remove(auxInfVarFilename)
        if(self.staticObsGiven == True):
            os.remove(auxStaticInfFilename)

        for widget in self.frameInfResults.winfo_children():
             widget.destroy()

        textInfo = scrolledtext.ScrolledText(self.frameInfResults, height=27, width=45)
        textInfo.grid(row=1, column=4, rowspan=27, padx=7)
        textInfo.insert(END, self.infResult)

        return

    def changeAttOptions(self, newOptionsList):

        self.attTab3.destroy()

        self.attTab3Choices = newOptionsList

        self.attTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired attribute: ", self.widthLeft, self.attTab3TkVar, self.attTab3Choices, self.attTab3Choices[0], 3, 1 )

    def changeIdsOptions(self, newOptionsList):

        self.idTab3.destroy()

        self.idTab3Choices = newOptionsList

        self.idTab3 = ElemTwoSelect(self.framePredictSpecific, "Desired id: ", self.widthLeft, self.idTab3TkVar, self.idTab3Choices, self.idTab3Choices[0], 2, 1 )

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
    
    def setDBNFile(self, dbnFilename):
        self.showDBN.destroy()
        self.showDBN = ElemTwoInputPresent(self.framePredictSpecific, "sdtDBN being used: ", dbnFilename, self.widthLeft, self.widthCenter, 1, 1)
        return

    def checkArgs(self):
        for widget in self.frameErrors.winfo_children():
            widget.destroy()

        if (self.showDBN.messageRight == "No file yet selected" ):
            printInfo = ttk.Label(self.frameErrors, text="No DBN was selected!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False

        if(self.idTab3TkVar.get() == 'Inference observations not given!'):
            printInfo = ttk.Label(self.frameErrors, text="Inference observations not given!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False
        
        if(self.attTab3TkVar.get() == 'There is not an sdtDBN learned!'):
            printInfo = ttk.Label(self.frameErrors, text="No attribute was specified!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False
        
        if(self.is_integer(self.timestepTab3.entry.get()) == False):
            printInfo = ttk.Label(self.frameErrors, text = "Timestep is not an integer!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=2)
            return False

        if(int(self.timestepTab3.entry.get()) < 1):
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