from tkinter import *

from utils.ElemThree import *
from utils.ElemTwoSelect import *


class Tab2:

    def __init__(self, mainFrame, width, tab3):
        self.tab3 = tab3

        self.frameObsInf = Frame(mainFrame, width=width)
        self.frameObsInf.grid(row=1, column=1, rowspan=2)

        # Dynamic and static observations files to inference
        self.dynObsInf = ElemThree(self.frameObsInf, 1, 1, "File with dynamic observations for inference: ", "Not yet selected!", 35)
        self.staticObsInf = ElemThree(self.frameObsInf, 2, 1, "File with static observations for inference: ", "Not yet selected!", 35)

        # Create a Tkinter variable for modes
        self.modeInfTkVar = StringVar(self.frameObsInf)
        self.modeInfChoices = [ 'Most probable value', 'Random estimation according to probability distribution' ]

        # Mode to predict values of attributes
        self.modeInf = ElemTwoSelect(self.frameObsInf, "Predict values of variables with: ", 35, self.modeInfTkVar, self.modeInfChoices, self.modeInfChoices[0], 3, 1 )

        # Button to submit all, creating a sdtDBN
        self.buttonSubmitObsInf = Button(self.frameObsInf, text = "Submit", borderwidth = 10, width=40, command=self.onSubmit)
        self.buttonSubmitObsInf.grid(row=4, column=1, columnspan=3, sticky = N+S+E+W)

    def onSubmit(self):
        self.tab3.getInfSpecs(self.dynObsInf.FileName, self.staticObsInf.FileName, self.modeInfTkVar.get())
        return





