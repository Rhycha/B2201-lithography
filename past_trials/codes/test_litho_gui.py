#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg

#======================
# Window
#======================
# Create instance
win = tk.Tk()
# Add a title
win.title("Python GUI")

def _destroyWindow():
    win.quit()
    win.destroy()

#======================
# Tab Control
#======================
tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Main tab
tabControl.add(tab1, text='Tab 1')      # Make First tab visible

tab2 = ttk.Frame(tabControl)            # Setting tab
tabControl.add(tab2, text='Tab 2')      # Make second tab visible

tab3 = ttk.Frame(tabControl) #lithography tab
tabControl.add(tab3, text='Tab 3')

tabControl.pack(expand=1, fill="both")  # Pack to make visible and fill entire window



#======================
# Tab 1
#======================
# LabelFrame using tab1 as the parent
mighty = ttk.LabelFrame(tab1, text=' Mighty Python ')
mighty.grid(column=0, row=0, padx=8, pady=4)

# Modify adding a Label using mighty as the parent instead of win
a_label = ttk.Label(mighty, text="Enter a name:")
a_label.grid(column=0, row=0, sticky='W')

#======================
# Tab 1 - Top Frame
#======================
# Make Frame for Top
frame1 = ttk.LabelFrame(mighty, text='Top Frame')
frame1.grid(column=0, row=0)

# Click Function
def click_me1():
    pass

def click_me2():
    pass

def click_me3():
    pass

# Adding a Button under the Top Frame
action1 = ttk.Button(frame1, text="Click Me!", command=click_me1)
action2 = ttk.Button(frame1, text="Click Me!", command=click_me2)
action3 = ttk.Button(frame1, text="Click Me!", command=click_me3)

# Positioning
f1_chil = frame1.winfo_children()
for child in f1_chil:
    child.grid(row=0, column=f1_chil.index(child))





#======================
# Tab 2
#======================


#======================
# Buttons
#======================

def start(object):
    pass

def pause(object):
    pass

def conti(object):
    pass

def stop(object):
    pass

#=====================
# Tab 3
#=====================
tab3_frame = tk.Frame(tab3, bg='blue')
tab3_frame.pack()
for orange_color in range(2):
    canvas = tk.Canvas(tab3_frame, width=150, height=80, highlightthickness=0, bg='orange')
    canvas.grid(row=orange_color, column=orange_color)


#======================
# Message Box
#======================


#======================
# Preprocessing UI
#======================
something = tk.Toplevel()
something.overrideredirect(True)

#======================
# Start GUI
#======================
win.mainloop()


