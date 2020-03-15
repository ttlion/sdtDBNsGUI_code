from tkinter import *

from utils.ElemThree import *
from utils.ElemTwoSelect import *
from utils.ElemTwoPresent import *


class Tab2:

    def __init__(self, mainFrame, width, tab3, tab4, tab5):
        self.tab3 = tab3
        self.tab4 = tab4
        self.tab5 = tab5

        self.widthLeft = 45
        self.widthCenter = 15
        self.widthInput = 4
        self.widthButton = 10

        self.frameObsInf = ttk.Frame(mainFrame, width = width)
        self.frameObsInf.grid(row=1, column=1, rowspan = 6)

        self.showDBN = ElemTwoPresent(self.frameObsInf, "sdtDBN being used: ", "No file yet selected", self.widthLeft, 1, 1)

        self.onlyCSVfiles = [("csv files", "*.csv" )]

        # Dynamic and static observations files to inference
        self.dynObsInf = ElemThree(self.frameObsInf, 2, 1, "File with dynamic observations for inference: ", "Not yet selected!", self.widthLeft, self.widthCenter, self.onlyCSVfiles)
        self.staticObsInf = ElemThree(self.frameObsInf, 3, 1, "File with static observations for inference: ", "Not yet selected!", self.widthLeft, self.widthCenter, self.onlyCSVfiles)

        self.hasStatic = True # By default assume this

        # Button to submit all, creating a sdtDBN
        self.buttonSubmitObsInf = ttk.Button(self.frameObsInf, text = "Submit", command=self.onSubmit)
        self.buttonSubmitObsInf.grid(row=4, column=1, columnspan=3, sticky = N+S+E+W)

        self.frameErrors = ttk.Frame(self.frameObsInf, width = width)
        self.frameErrors.grid(row=5, column=1, rowspan=3)

    def onSubmit(self):

        if( self.checkArgs() == False):
            return

        printInfo = ttk.Label(self.frameErrors, text="Files with observations submited!", style="ok.TLabel")
        printInfo.grid(row=2, column=1, columnspan=3)

        self.tab3.getInfSpecs(self.dynObsInf.FileName, self.staticObsInf.FileName)
        self.tab4.getInfSpecs(self.dynObsInf.FileName, self.staticObsInf.FileName)
        self.tab5.getInfSpecs(self.dynObsInf.FileName, self.staticObsInf.FileName)
        return

    def setDBNFile(self, dbnFilename, hasStatic: bool):
        self.showDBN.destroy()
        self.showDBN = ElemTwoPresent(self.frameObsInf, "sdtDBN being used: ", dbnFilename, self.widthLeft, 1, 1)
        
        self.hasStatic = hasStatic

        self.staticObsInf.destroy()
        self.staticObsInf.FileName = ''

        if (self.hasStatic == True):
            self.staticObsInf = ElemThree(self.frameObsInf, 3, 1, "File with static observations for inference: ", "Not yet selected!", self.widthLeft, self.widthCenter, self.onlyCSVfiles)
        return

    def checkArgs(self):
        for widget in self.frameErrors.winfo_children():
            widget.destroy()

        if (self.showDBN.messageRight == "No file yet selected" ):
            printInfo = ttk.Label(self.frameErrors, text="No DBN was selected!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=3)
            return False

        if(self.dynObsInf.FileName == "Not yet selected!" or self.dynObsInf.FileName == '' ):
            printInfo = ttk.Label(self.frameErrors, text="No file with dynamic observations was given", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=3)
            return False
        
        if( self.staticObsInf.FileName == "Not yet selected!" or ( self.staticObsInf.FileName == '' and self.hasStatic == True ) ):
            printInfo = ttk.Label(self.frameErrors, text="No file with static observations was given, just using the dynamic observations", style="ok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=3)

        return True




