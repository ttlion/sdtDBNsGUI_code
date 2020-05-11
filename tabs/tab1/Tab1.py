from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

from tabs.tab1.PageElements import *
from tabs.tab1.LearnDBN import *

class Tab1:

    def __init__(self, mainFrame, width, tab1_2, tab2, tab3, tab4, tab5):
        self.tab1_2 = tab1_2
        self.tab2 = tab2
        self.tab3 = tab3
        self.tab4 = tab4
        self.tab5 = tab5

        self.widthLeft = 50
        self.widthCenter = 15
        self.widthInput = 4

        self.mainFrame = mainFrame

        self.dbnLearnFrame = ttk.Frame(mainFrame, width=width)
        self.dbnLearnFrame.grid(row=1, column=1, rowspan=10)

        self.pageElemts = PageElem()

        onlyCSVfiles = [("csv files", "*.csv" )]

        self.dynObs = ElemThree(self.dbnLearnFrame, 1, 1, "File with dynamic observations: ", "Not yet selected!", self.widthLeft, self.widthCenter, onlyCSVfiles )
        self.staticObs = ElemThree(self.dbnLearnFrame, 2, 1, "File with static observations: ", "Not yet selected!", self.widthLeft, self.widthCenter, onlyCSVfiles)

        self.pageElemts.addElem("dynObs", self.dynObs)
        self.pageElemts.addElem("staticObs", self.staticObs)

        self.markovLag = ElemTwoInput(self.dbnLearnFrame, "Markov lag: ", self.widthLeft, self.widthInput, 3, 1, 1)
        self.maxParentsPast = ElemTwoInput(self.dbnLearnFrame, "Max parents from past: ", self.widthLeft, self.widthInput, 4, 1, 1)
        self.maxStaticParents = ElemTwoInput(self.dbnLearnFrame, "Max static parents: ", self.widthLeft, self.widthInput, 5, 1, 1)

        self.pageElemts.addElem("markovLag", self.markovLag)
        self.pageElemts.addElem("pValue", self.maxParentsPast)
        self.pageElemts.addElem("bValue", self.maxStaticParents)

        # Create a Tkinter variable for scoring functions, define its choices
        self.sfTkVar = StringVar(self.dbnLearnFrame)
        self.sfChoices = [ 'Log-Likelihood (LL)', 'Minimum Description Length (MDL)' ]

        # Create a Tkinter variable for stationary or not functions, define its choices
        self.statTkVar = StringVar(self.dbnLearnFrame)
        self.statChoices = [ 'yes', 'no' ]

        self.sf = ElemTwoSelect(self.dbnLearnFrame, "Scoring Function: ", self.widthLeft, self.sfTkVar, self.sfChoices, self.sfChoices[0], 6, 1 )
        self.stationary = ElemTwoSelect(self.dbnLearnFrame, "Stationary sdtDBN?: ", self.widthLeft, self.statTkVar, self.statChoices, self.statChoices[0], 7, 1 )

        self.pageElemts.addElem("sfValue", self.sf)
        self.pageElemts.addElem("stationaryValue", self.stationary)

        self.fileToSave = ElemTwoInput(self.dbnLearnFrame, "File to save the learned sdtDBN: ", self.widthLeft, self.widthCenter, 8, 1, 'exampleFile.txt')
        self.pageElemts.addElem("fileToSave", self.fileToSave)

        self.mA_dynPast = ElemThree(self.dbnLearnFrame, 9, 1, "File with mandatory parents from previous timesteps: ", "Not yet selected!", self.widthLeft, self.widthCenter, onlyCSVfiles )
        self.mA_dynSame = ElemThree(self.dbnLearnFrame, 10, 1, "File with mandatory parents from the same timestep: ", "Not yet selected!", self.widthLeft, self.widthCenter, onlyCSVfiles )
        self.mA_static = ElemThree(self.dbnLearnFrame, 11, 1, "File with mandatory static parents: ", "Not yet selected!", self.widthLeft, self.widthCenter, onlyCSVfiles )
        
        self.pageElemts.addElem("mA_dynPast", self.mA_dynPast)
        self.pageElemts.addElem("mA_dynSame", self.mA_dynSame)
        self.pageElemts.addElem("mA_static", self.mA_static)

        self.mNotA_dynPast = ElemThree(self.dbnLearnFrame, 12, 1, "File with forbidden parents from previous timesteps: ", "Not yet selected!", self.widthLeft, self.widthCenter, onlyCSVfiles )
        self.mNotA_dynSame = ElemThree(self.dbnLearnFrame, 13, 1, "File with forbidden parents from the same timestep: ", "Not yet selected!", self.widthLeft, self.widthCenter, onlyCSVfiles )
        self.mNotA_static = ElemThree(self.dbnLearnFrame, 14, 1, "File with forbidden static parents: ", "Not yet selected!", self.widthLeft, self.widthCenter, onlyCSVfiles )
        
        self.pageElemts.addElem("mNotA_dynPast", self.mNotA_dynPast)
        self.pageElemts.addElem("mNotA_dynSame", self.mNotA_dynSame)
        self.pageElemts.addElem("mNotA_static", self.mNotA_static)


        self.learnSubmit = LearnDBN(self.dbnLearnFrame, "Create sdtDBN", 15, 1, self.pageElemts, tab1_2, tab2, tab3, tab4, tab5)
