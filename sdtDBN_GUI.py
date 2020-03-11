#########################################
# Imports

from os import path

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

if (path.exists("ist_logo_icon.ico")): # Just safety guard
    root.iconbitmap("ist_logo_icon.ico")

##################################################################################
##################################################################################
##################################################################################
##################################################################################
# Program styling definittions

#########################################
# Some fonts

font_tabs = ("Times", 11)
font_tabs_bold = ("Times", 10, "bold")

font_bold = ("Times", 12, "bold")
font_italic = ("Times", 11, "italic")

font_insert = ("Times", 13, "bold")
font_insertButton = ("Times", 14, "bold")

font_ok_notok = ("Times", 11, "bold italic")

#########################################
# Creation of style object

s = ttk.Style()
s.theme_use('clam')

#########################################
# Tabs styling
s.configure("TNotebook.Tab", padding = (10, 3, 10, 3), relief = "flat",  background = "#FF4500", font = font_tabs, bordercolor = "#FF007F", focuscolor = "None")
s.map('TNotebook.Tab', background = [('selected','red')], font = [('selected', font_tabs_bold), ('active', font_tabs_bold)])

#########################################
# Notebook styling
s.configure("TNotebook", background = "white", bordercolor = "#FF007F", padding = (5,5,5,5)) 

#########################################
# Frames styling
s.configure("TFrame", background = "#FFCCCC") # Set all frames with same color

#########################################
# Styling of labels
s.configure("ask.TLabel", background = "#FFCCCC", font = font_bold, foreground = "#FF4500")
s.configure("filenames.TLabel", background = "#FFCCCC", font = font_italic)
s.configure("ok.TLabel", background = "#FFCCCC", font = font_ok_notok, foreground = "green")
s.configure("notok.TLabel", background = "#FFCCCC", font = font_ok_notok, foreground = "red")

#########################################
# Styling of entries
s.configure("TEntry", background = "#FFCCCC", foreground = "#FF4500", fieldbackground = "#FFCCCC", bordercolor = "#FFCCCC")
s.map("TEntry", fieldbackground = [('focus','white')] , foreground = [('focus','black')], bordercolor = [('focus','black')] )

#########################################
# Styling of buttons
s.configure('TButton', background = '#FFCCCC', foreground = 'black', font = font_bold, bordercolor = "#FF4500", focuscolor = "None", padding = (0, 7, 0, 7))
s.map('TButton', foreground = [('active','#FF4500')], font = [('active', font_insertButton)] ) 

#########################################
# Styling of option menus
s.configure('TMenubutton', background = '#FFCCCC', foreground = 'black', font = font_bold, bordercolor = "#FF4500", focuscolor = "None", padding = (10, 10, 10, 10), arrowsize = 2)
s.map('TMenubutton', foreground = [('active','#FF4500')]) 

##################################################################################
##################################################################################
##################################################################################
##################################################################################
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
tab2 = Tab2(tabControl, 200, tab3, tab4, tab5)
tab1 = Tab1(tabControl, 200, tab2, tab3, tab4, tab5)

#########################################
# Create TAB menu

tabControl.add(tab1.dbnLearnFrame, text="Learn DBN from data")
tabControl.add(tab2.frameObsInf, text="Observations to Inference")
tabControl.add(tab3.framePredictSpecific, text="Predict attribute distribution")
tabControl.add(tab4.framePredictProgres, text="Predict progression")
tabControl.add(tab5.framePredictMany, text="Predictions for many IDs")
tabControl.grid(row=1, column=1, rowspan=10)

#########################################
# Mainloop of program
root.mainloop()
