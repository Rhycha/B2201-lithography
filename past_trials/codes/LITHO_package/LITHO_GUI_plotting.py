from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =======================
# self.tabSetting-frameSetting3 (Lithography)
# =======================

class Plotting():

    def __init__(self, GUI):
        self.gui = GUI
        self.createGraph()

    def createGraph(self):

        self.fig = Figure(figsize=(12, 5), facecolor='white')

        axis = self.fig.add_subplot(111)  # 1 row, 1 column

        xValues = [1, 2, 3, 4]
        yValues0 = [6, 7.5, 8, 7.5]
        yValues1 = [5.5, 6.5, 8, 6]
        yValues2 = [6.5, 7, 8, 7]

        t0, = axis.plot(xValues, yValues0, color='purple')  # change the color of the plotted line
        t1, = axis.plot(xValues, yValues1, color='red')
        t2, = axis.plot(xValues, yValues2, color='blue')

        axis.set_ylabel('Vertical Label')
        axis.set_xlabel('Horizontal Label')

        axis.grid()

        self.fig.legend((t0, t1, t2), ('First line', 'Second line', 'Third line'), 'upper right')
        canvas = FigureCanvasTkAgg(self.fig, master=self.gui.frameSensorGraph)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

