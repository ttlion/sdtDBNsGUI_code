from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

from tabs.tab1.PageElements import *
from tabs.tab1.LearnDBN import *



class Tab1:

    def __init__(self, mainFrame, width):
        self.mainFrame = mainFrame

        self.dbnLearnFrame = Frame(mainFrame, width=width)
        self.dbnLearnFrame.grid(row=1, column=1, rowspan=10)

        self.pageElemts = PageElem()

        self.dynObs = ElemThree(self.dbnLearnFrame, 1, 1, "File with dynamic observations: ", "Not yet selected!", 25)
        self.staticObs = ElemThree(self.dbnLearnFrame, 2, 1, "File with static observations: ", "Not yet selected!", 25)

        self.pageElemts.addElem("dynObs", self.dynObs)
        self.pageElemts.addElem("staticObs", self.staticObs)

        self.markovLag = ElemTwoInput(self.dbnLearnFrame, "Markov lag: ", 25, 5, 3, 1)
        self.maxParentsPast = ElemTwoInput(self.dbnLearnFrame, "Max parents from past: ", 25, 5, 4, 1)
        self.maxStaticParents = ElemTwoInput(self.dbnLearnFrame, "Max static parents: ", 25, 5, 5, 1)

        self.pageElemts.addElem("markovLag", self.markovLag)
        self.pageElemts.addElem("pValue", self.maxParentsPast)
        self.pageElemts.addElem("bValue", self.maxStaticParents)

        # Create a Tkinter variable for scoring functions, define its choices
        self.sfTkVar = StringVar(self.dbnLearnFrame)
        self.sfChoices = [ 'Log-Likelihood (LL)', 'Minimum Description Length (MDL)' ]

        # Create a Tkinter variable for stationary or not functions, define its choices
        self.statTkVar = StringVar(self.dbnLearnFrame)
        self.statChoices = [ 'yes', 'no' ]

        self.sf = ElemTwoSelect(self.dbnLearnFrame, "Scoring Function: ", 25, self.sfTkVar, self.sfChoices, self.sfChoices[0], 6, 1 )
        self.stationary = ElemTwoSelect(self.dbnLearnFrame, "Stationary sdtDBN?: ", 25, self.statTkVar, self.statChoices, self.statChoices[0], 7, 1 )

        self.pageElemts.addElem("sfValue", self.sf)
        self.pageElemts.addElem("stationaryValue", self.stationary)

        self.learnSubmit = LearnDBN(self.dbnLearnFrame, "Create sdtDBN", 40, 8, 1, self.pageElemts)
