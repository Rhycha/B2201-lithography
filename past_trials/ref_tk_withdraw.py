#Import the library
from tkinter import *
from tkinter import ttk

#Create an instance of Tkinter frame
win= Tk()

#Set the window geometry
win.geometry("750x200")

#Create a Label
Label(win, text= "Tkinter is a GUI Library in Python", font=('Helvetica 15 bold')).pack(pady=20)

#Define a function to show the Main window
def show_win():
   win.deiconify()

#Create another Toplevel Window
new_win= Toplevel(win)
new_win.geometry("700x250")
new_win.title("NEW WINDOW")

#Hide the Main Window
win.withdraw()

#Create a Button to Hide/ Reveal the Main Window
button= ttk.Button(new_win, text="Show" ,command= show_win)
button.pack(pady=50)

win.mainloop()