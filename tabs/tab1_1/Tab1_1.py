from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import re

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

        # Printing success/error messages
        self.submitionframe = ttk.Frame(self.dbnLearnFileFrame, width = width)
        self.submitionframe.grid(row=3, column=1, columnspan=3)
        
        # Present DBN attributes
        self.presentDBNAttsFrame = ttk.Frame(self.dbnLearnFileFrame, width=50)
        self.presentDBNAttsFrame.grid(row=1, column=4, rowspan=10)

        # Present DBN structure and parameters
        self.presentDBNFrame = ttk.Frame(self.dbnLearnFileFrame, width=50)
        self.presentDBNFrame.grid(row=1, column=5, rowspan=10)

        self.fileWithObj = ElemThree(self.dbnLearnFileFrame, 1, 1, "File with sdtDBN object: ", "Not yet selected!", self.widthLeft, self.widthCenter, [("all formats", "*.*")] )

        # Button to submit file
        self.buttonSubmitFile = ttk.Button(self.dbnLearnFileFrame, text = "Submit file", command = self.onSubmit)
        self.buttonSubmitFile.grid(row=2, column=1, columnspan=3, sticky = N+S+E+W)

        # Initialize some data structs
        self.dynAttList = []
        self.staticAttList = []
        self.hasStatic = False

    def onSubmit(self):

        for widget in self.submitionframe.winfo_children():
            widget.destroy()

        for widget in self.presentDBNAttsFrame.winfo_children():
            widget.destroy()

        for widget in self.presentDBNFrame.winfo_children():
            widget.destroy()

        if( self.checkArgs() == False ):
            return

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        p = subprocess.Popen(['java', '-jar', 'sdtDBN_v0_0_1.jar', '-fromFile', self.fileWithObj.FileName, '-d' ], startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')

        auxText_getAtts = p.stdout.read()

        p.terminate()

        # Reinitialize these lists
        self.dynAttList = []
        self.staticAttList = []

        # Get static and dynamic attributes of DBN
        for line in auxText_getAtts.splitlines():
            result = re.search(r'label\=\"(.*)\[0\]"', line) # Find the dynamic attributes
            if result is not None:
                self.dynAttList.append(result.group(1))

            result1 = re.search(r'^(.*)\[shape\=polygon', line) # Find the static attributes
            if result1 is not None:
                self.staticAttList.append(result1.group(1))

        p = subprocess.Popen(['java', '-jar', 'sdtDBN_v0_0_1.jar', '-fromFile', self.fileWithObj.FileName ], startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf-8')

        self.learnedsdtDBN_text = p.stdout.read()

        p.terminate()

        printInfo = ttk.Label(self.submitionframe, text="sdtDBN retrieved from file!", style="ok.TLabel")
        printInfo.grid(row=1, column=1, columnspan=3)

        if(len(self.staticAttList) != 0):
            self.hasStatic = True
        else:
            self.hasStatic = False

        self.presentOutputToUser()
        self.giveArgsToOtherTabs()

        return

    def checkArgs(self):
        if(self.fileWithObj.FileName == "Not yet selected!" or self.fileWithObj.FileName == ''):
            printInfo = ttk.Label(self.submitionframe, text="no sdtDBN file was given!", style="notok.TLabel")
            printInfo.grid(row=1, column=1, columnspan=3)
            return False
        return True
 
    def presentOutputToUser(self):
        self.presentAttsToUser()

        textInfo = scrolledtext.ScrolledText(self.presentDBNFrame, height=27, width=45)
        textInfo.grid(row=1, column=1, rowspan=27, padx=7)
        textInfo.insert(END, self.learnedsdtDBN_text)

    def presentAttsToUser(self):
        textInfo = scrolledtext.ScrolledText(self.presentDBNAttsFrame, height=27, width=15)
        textInfo.grid(row=1, column=1, rowspan=27, padx=7)
        textInfo.insert(END, "Dynamic Atts:\n")
        for element in self.dynAttList:
            textInfo.insert(END, element + "\n")

        if(self.hasStatic == True):
            textInfo.insert(END, "\nStatic Atts:\n")
            for element in self.staticAttList:
                textInfo.insert(END, element + "\n")
    
    def giveArgsToOtherTabs(self):

        self.tab2.setDBNFile(self.fileWithObj.FileName, self.hasStatic)
        self.tab3.setDBNFile(self.fileWithObj.FileName)
        self.tab4.setDBNFile(self.fileWithObj.FileName)
        self.tab5.setDBNFile(self.fileWithObj.FileName)

        self.tab3.changeAttOptions(self.dynAttList)
        self.tab4.changeAttOptions(self.dynAttList)
