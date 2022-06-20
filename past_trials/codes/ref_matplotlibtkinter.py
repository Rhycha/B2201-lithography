"""
===============
Embedding in Tk
===============

"""

import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import numpy as np
import matplotlib.pyplot as plt
from LITHO_package.LITHO_GUI_SQLite import *
from matplotlib.figure import Figure

root = tk.Tk()
root.wm_title("Embedding in Tk")

frame1 = tk.Frame(master=root)
frame2 = tk.Frame(master=root)
frame1.grid(row=0, column=0)
frame2.grid(row=0, column=1)

fig = Figure(figsize=(5, 4), dpi=100)

t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=frame1)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, frame1)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
sql=SQLite()
df = sql.fetchMeasuresAtLastTrial_id2()
# df.set_index('MeasuringTime')
df2 = df["Ampere"]
print(df)
df.plot()
df2.plot()
plt.show()

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tk.Button(master=frame1, text="Quit", command=_quit)
button.pack(side=tk.BOTTOM)



tk.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.