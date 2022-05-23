import common
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
import enum
import threading

root = tk.Tk()
root.wm_geometry("800x480")
root.resizable(False, False)
root.attributes('-fullscreen', True)

frameSplash = tk.Frame(root, height = 480, width = 800, bg = "black")
frameSplash.place(x = 0, y = 0)



#tempImage = PhotoImage(file="gearImage.png")
#tempImage = tempImage.subsample(6, 6)
tempImage = PhotoImage(file = "cella_logo.png")
tempImage = tempImage.subsample(2, 2)
labelTemp = tk.Label(frameSplash, image = tempImage, bg = "black")
labelTemp.place(in_ = frameSplash, x = 0, y = 0, width = 800, height = 480)

frameSplash.lift()

root.mainloop()
