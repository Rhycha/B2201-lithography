import tkinter as tk
import tkinter.ttk as ttk
from LITHO_GUI_plotting import Plotting

class miniGUI():

    def __init__(self):

        self.root = tk.Tk()

        self.createWidget()
        PlotCallback = Plotting(self)

        PlotCallback.createGraph()
    def _quit(self):
        self.root.quit()
        self.root.destroy()
        exit()


    def createWidget(self):

        # Tab Control introduced here --------------------------------------
        tabControl = ttk.Notebook(self.root)  # Create Tab Control

        tab1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab1, text='Calibraiton')    # Add the tab -- COMMENTED OUT FOR CH08

        # tab2 = ttk.Frame(tabControl)  # Add a second tab
        # tabControl.add(tab2, text='Widgets')  # Make second tab visible
        #
        tabControl.pack(expand=1, fill="both")  # Pack to make visible
        # ~ Tab Control introduced here -----------------------------------------

        # --------- Calibration main frame
        self.frameCali = tk.Frame(tab1)
        self.frameCali.grid(column=0, row=0)


        # --------- Calibration subframe
        self.frameCaliButtons = tk.Frame(self.frameCali)
        self.frameCaliGraphs =tk.Frame(self.frameCali)
        self.frameCaliButtons.grid(column=6, row=0)
        self.frameCaliGraphs.grid(column=0, row=0, columnspan=5)


        # --------- Calibration buttons
        self.buttonCaliSensor = tk.Button(self.frameCaliButtons, text="Sensor")
        self.buttonCaliAmpere = tk.Button(self.frameCaliButtons, text="Ampere")
        self.buttonCaliTemp = tk.Button(self.frameCaliButtons, text="Temp")
        self.buttonCaliWatt = tk.Button(self.frameCaliButtons, text="Watt")

        self.buttonCaliSensor.grid(column=0, row=0)
        self.buttonCaliAmpere.grid(column=0, row=1)
        self.buttonCaliTemp.grid(column=0, row=2)
        self.buttonCaliWatt.grid(column=0, row=3)


        # ---------- Calibration graphs
        self.frameSensorGraph = tk.LabelFrame(self.frameCaliGraphs,text="SensorGraph")
        self.frameAmpereGraph = tk.Frame(self.frameCaliGraphs)
        self.frameTempGraph = tk.Frame(self.frameCaliGraphs)
        self.frameWattGraph = tk.Frame(self.frameCaliGraphs)

        self.frameSensorGraph.pack(fill="both")
        # self.frameAmpereGraph.grid(column=0, row=0)


if (__name__=="__main__"):
    gui = miniGUI()
    gui.root.mainloop()