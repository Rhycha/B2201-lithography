import tkinter as tk
import tkinter.simpledialog
root = tk.Tk() # dialog needs a root window, or will create an "ugly" one for you
root.withdraw()
password = tkinter.simpledialog.askstring("Password", "Enter password:", show='*')
root.destroy()