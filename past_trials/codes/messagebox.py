from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
# import os #for relative path



root = Tk()
root.title("Cella Biotech Lithography Software")
root.iconbitmap('../images/cella_logo.ico')

def cali_needed_popup():

	messagebox.showinfo( "cali_needed_popup",\
		"For better performance, Execute calibration\n\n\
Path : Settings - Calibration - Start \
	 ")

Button(root, text="Calibration Needed Test", command=cali_needed_popup).pack()

mainloop()