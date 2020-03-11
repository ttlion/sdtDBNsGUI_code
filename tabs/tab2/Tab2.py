from tkinter import *

from utils.ElemThree import *
from utils.ElemTwoSelect import *


class Tab2:

    def __init__(self, mainFrame, width, tab3, tab4, tab5):
        self.tab3 = tab3
        self.tab4 = tab4
        self.tab5 = tab5

        self.widthLeft = 45
        self.widthCenter = 15
        self.widthInput = 4
        self.widthButton = 10

        self.frameObsInf = ttk.Frame(mainFrame, width=width)
        self.frameObsInf.grid(row=1, column=1, rowspan=2)

        # Dynamic and static observations files to inference
        self.dynObsInf = ElemThree(self.frameObsInf, 1, 1, "File with dynamic observations for inference: ", "Not yet selected!", self.widthLeft, self.widthCenter)
        self.staticObsInf = ElemThree(self.frameObsInf, 2, 1, "File with static observations for inference: ", "Not yet selected!", self.widthLeft, self.widthCenter)

        # Button to submit all, creating a sdtDBN
        self.buttonSubmitObsInf = ttk.Button(self.frameObsInf, text = "Submit", command=self.onSubmit)
        self.buttonSubmitObsInf.grid(row=4, column=1, columnspan=3, sticky = N+S+E+W)

    def onSubmit(self):
        self.tab3.getInfSpecs(self.dynObsInf.FileName, self.staticObsInf.FileName)
        self.tab4.getInfSpecs(self.dynObsInf.FileName, self.staticObsInf.FileName)
        self.tab5.getInfSpecs(self.dynObsInf.FileName, self.staticObsInf.FileName)
        return

    def setStatic(self, hasStatic: bool):
        self.staticObsInf.destroy()
        if (hasStatic == True):
            self.staticObsInf = ElemThree(self.frameObsInf, 2, 1, "File with static observations for inference: ", "Not yet selected!", self.widthLeft, self.widthCenter)
        return





