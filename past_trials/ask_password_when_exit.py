#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# protocolHandler.py
import tkinter as tk
from tkinter import *
import tkinter.messagebox

# handle WM_DELETE_WINDOW event
def handleProtocol():
    # open a dialog
    if tk.messagebox.askokcancel("Notice", "Are you sure to close the window"):
       # close the application
       win.destroy()

# create the main window
win = Tk()


# create a protocal
win.protocol("WM_DELETE_WINDOW", handleProtocol)
win.mainloop()

