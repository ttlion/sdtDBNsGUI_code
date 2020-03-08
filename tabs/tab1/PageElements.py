from tkinter import *

class PageElem:

    def __init__(self):
        self.elements = { }

    def addElem(self, name, element):
        self.elements[name] = element

    def removeElem(self, name):
        self.elements.pop(name, None)

    def getElem(self, name):
        return self.elements[name]