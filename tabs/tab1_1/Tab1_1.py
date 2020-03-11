from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

from tabs.tab1.PageElements import *
from tabs.tab1.LearnDBN import *



class Tab1_1:

    def __init__(self, mainFrame, width, tab2, tab3, tab4, tab5):
        self.tab2 = tab2
        self.tab3 = tab3
        self.tab4 = tab4
        self.tab5 = tab5

        self.widthLeft = 30
        self.widthCenter = 15

        self.mainFrame = mainFrame

        self.dbnLearnFileFrame = ttk.Frame(mainFrame, width = width)
        self.dbnLearnFileFrame.grid(row=1, column=1, rowspan=10)

        self.dynObs = ElemThree(self.dbnLearnFileFrame, 1, 1, "File with sdtDBN object: ", "Not yet selected!", self.widthLeft, self.widthCenter )

        # Button to submit file
        self.buttonSubmitFile = ttk.Button(self.dbnLearnFileFrame, text = "Submit file", command = self.onSubmit)
        self.buttonSubmitFile.grid(row=2, column=1, columnspan=3, sticky = N+S+E+W)

    def onSubmit(self):
        return

