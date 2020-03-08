#########################################
# Imports

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from mainMenu.Menu import *

from utils.ElemThree import *
from utils.ElemTwoInput import *
from utils.ElemTwoSelect import *

from tabs.tab1.PageElements import *
from tabs.tab1.LearnDBN import *
from tabs.tab1.Tab1 import *

from tabs.tab2.Tab2 import *

from tabs.tab3.Tab3 import *

from tabs.tab4.Tab4 import *

from tabs.tab5.Tab5 import *

#########################################
# Root of program made with tkinter lib

root = Tk()
root.title("sdtDBNs GUI")

#########################################
# Main menu bar
windowMenu = MyMenu(root)

#########################################
# Define tab environment
tabControl = ttk.Notebook(root)

#########################################
# Create the several tabs

tab5 = Tab5(tabControl, 200)
tab4 = Tab4(tabControl, 200)
tab3 = Tab3(tabControl, 200)
tab2 = Tab2(tabControl, 200, tab3, tab4)
tab1 = Tab1(tabControl, 200, tab3, tab4)

#########################################
# Create TAB menu

tabControl.add(tab1.dbnLearnFrame, text="Learn DBN from data")
tabControl.add(tab2.frameObsInf, text="Observations to Inference")
tabControl.add(tab3.framePredictSpecific, text="Predict attribute value")
tabControl.add(tab4.framePredictProgres, text="Predict progression")
tabControl.add(tab5.framePredictMany, text="Predictions for many IDs")
tabControl.grid(row=1, column=1, rowspan=10)

#########################################
# Mainloop of program
root.mainloop()
