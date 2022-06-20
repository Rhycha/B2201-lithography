
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
# import serial #circuitpython 설치해야 module 지원
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from LITHO_package.LITHO_GUI_Callbacks import *
from LITHO_package.LITHO_Design import *
from LITHO_package.LITHO_GUI_Callbacks import *
from LITHO_package.LITHO_GUI_plotting import *
########################################
############# UI Section ##############
######################################


#================================
# Root
#===============================

class GUI():


    # ========================
    # Style
    # ========================

    def __init__(self):
        # Create instance

        self.root = tk.Tk()
        self.style = ttk.Style()

        # Add a title
        self.root.title("Lithography-Cella corp")
        self.root.wm_geometry("800x480")

        # Disable resizing the window
        self.root.resizable(False, False)

        # Make fullScreen
        self.root.attributes('-fullscreen', True)

        # Create Values
        self.createVariables()
        self.image_path = "../images/"

        # Create Status instance
        self.status = Status(self)


        # Callback methods now in different module
        self.callBacks = Callbacks(self, self.status)


        # Create all the Widgets
        self.createWidgets()

        # Create SQLite instance
        # self.SQLite = SQLite()


        # Create AsyncTask
        # self.atask = AsyncTask(self, self.status)


        # Style
        self.style.theme_create("customTabStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [20, 10], "background": colorBrightGray, "foreground": "white",
                              "font": ('family Calibri', '12', 'bold')},
                "map": {"background": [("selected", colorDarkGray)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        self.style.theme_use("customTabStyle")

        self.frameSplash.lift()

    def _quit(self):
        self.root.quit()
        self.root.destroy()
        exit()



    def createVariables(self):
        self.sensorValue = tk.DoubleVar()
        self.sensorValue.set(0)
        self.temperature = tk.DoubleVar()
        self.temperature.set(0)
        self.ledCurrent = tk.DoubleVar()
        self.ledCurrent.set(0)
        self.exposureTime = tk.DoubleVar()
        self.exposureTime.set(0)
        self.exposureEnergy = tk.DoubleVar()
        self.exposureEnergy.set(0)
        self.outputPower = tk.DoubleVar()
        self.outputPower.set(0)
        self.elapsedTime = tk.DoubleVar()
        self.elapsedTime.set(0)
        self.elapsedEnergy = tk.DoubleVar()
        self.elapsedEnergy.set(0)
        self.timeText = tk.StringVar()
        self.timeText.set("")
        self.energyText = tk.StringVar()
        self.energyText.set("")

    def createWidgets(self):
        # ================================
        # Root - All Frames
        # =================================
        #UI Component
        self.frameTop = tk.Frame(self.root, height=480, width=800, bg=colorDarkGray)
        self.frameButton = tk.Frame(self.root, height=290, width=800, bg=colorDarkGray)
        self.framePaused = tk.Frame(self.root, height=310, width=634, bg=colorIvory, highlightthickness=2,
                                    highlightbackground="gray")
        self.tabSetting = ttk.Notebook(self.root, width=800, height=480)
        self.frameSplash = tk.Frame(self.root, height=480, width=800, bg=colorDarkGray)


        # Positioning
        self.frameTop.place(x=0, y=0)
        self.frameButton.place(x=1, y=190)  ## to hide 1 pixel vertical line by self.tabSetting notebook widget

        self.tabSetting.place(x=0, y=0)
        self.frameSplash.place(x=0, y=0)

        #Binding
        self.tabSetting.bind("<<NotebookTabChanged>>", self.callBacks.tabChanged)


        #===============================
        # Root - self.frameTop
        #===============================
        # Variable
        self.gearImg = PhotoImage(file="../images/gearImageGraywithbg.png")
        # self.gearImg = PhotoImage(file=self.image_path+"gearImageGraywithbg.png")
        self.gearImg = self.gearImg.subsample(3, 3)

        # UI component
        self.frameTime = tk.Frame(self.frameTop, height=130, width=355, bg=colorBrightGray, highlightbackground="yellow")
        self.frameEnergy = tk.Frame(self.frameTop, height=130, width=355, bg=colorBrightGray, highlightbackground="yellow")
        self.labelEnergy1 = tk.Label(self.frameTop, text="Exposure Energy (mJ/cm²)", bg=colorBrightGray, fg="white",
                                     font=fontSmallLabel)
        self.labelEnergy2 = tk.Label(self.frameTop, textvariable=self.exposureEnergy, bg=colorBrightGray, fg="white",
                                     font=fontMiddleLabel)
        self.framePower = tk.Frame(self.frameTop, height=100, width=220, bg=colorDarkGray)
        self.frameCurrent = tk.Frame(self.frameTop, height=100, width=180, bg=colorDarkGray)
        self.frameTemper = tk.Frame(self.frameTop, height=100, width=180, bg=colorDarkGray)
        self.buttonStartStop = tk.Button(self.frameTop, highlightthickness=0, text="START", bg=colorGreen, fg="white",
                                         font=fontLargeLabel, activeforeground="white", activebackground=colorGreen,
                                         command=lambda: self.callBacks.KeyInputCheck("startStop"))
        self.buttonSetting = tk.Button(self.frameTop, highlightthickness=0, relief=tk.RAISED, image=self.gearImg, bg=colorDarkGray, command=lambda: self.callBacks.KeyInputCheck("setting"))
        self.labelSensor1 = tk.Label(self.frameTop, text="Sensor Value: ", bg=colorDarkGray, fg="white",
                                     font=fontSmallLabel)
        self.labelSensor2 = tk.Label(self.frameTop, textvariable=self.sensorValue, bg=colorDarkGray, fg="white", font=fontSmallLabel)
        self.labelExit = tk.Label(self.frameTop, bg=colorDarkGray)


        # Positioning
        self.frameTime.place(x=30, y=30, height=130, width=355)

        self.frameEnergy.place(x=415, y=30)
        self.labelEnergy1.place(in_=self.frameEnergy, x=10, y=10, width=335, height=30)
        self.labelEnergy2.place(in_=self.frameEnergy, x=10, y=45, width=335, height=70)

        self.framePower.place(x=30, y=350)


        self.frameCurrent.place(x=270, y=350)


        self.frameTemper.place(x=470, y=350)


        self.buttonStartStop.place(x=30, y=190, width=740, height=130)
        self.buttonSetting.place(x=670, y=350, width=100, height=100)

        self.labelSensor1.place(in_=self.frameTop, x=30, y=7, width=120, height=18)
        self.labelSensor2.place(in_=self.frameTop, x=150, y=7, width=150, height=18)

        self.labelExit.place(in_=self.frameTop, x=700, y=0, width=100, height=18)

        # Binding
        self.frameTime.bind("<Button-1>", lambda event: self.status.OpStatusChange("TIME_INPUT"))
        self.frameEnergy.bind("<Button-1>", lambda event: self.status.OpStatusChange("ENERGY_INPUT"))
        self.labelEnergy1.bind("<Button-1>", lambda event: self.status.OpStatusChange("ENERGY_INPUT"))
        self.labelEnergy2.bind("<Button-1>", lambda event: self.status.OpStatusChange("ENERGY_INPUT"))

        self.labelExit.bind("<Button-1>", lambda event: self.status.OpStatusChange("EXIT"))

        #==============================
        # Root - self.frameButton
        #==============================
        self.subframeButton1 = tk.Frame(self.frameButton, height=210, width=525, bg=colorDarkGray)
        self.subframeButton2 = tk.Frame(self.frameButton, height=210, width=210, bg=colorDarkGray)

        self.subframeButton1.place(in_=self.frameButton, x=20, y=25)
        self.subframeButton2.place(in_=self.frameButton, x=570, y=25)

        # Positioning
        self.subframeButton1.grid_propagate(0)
        self.subframeButton1.rowconfigure(0, weight=1)
        self.subframeButton1.rowconfigure(1, weight=1)
        self.subframeButton1.columnconfigure(0, weight=1)
        self.subframeButton1.columnconfigure(1, weight=1)
        self.subframeButton1.columnconfigure(2, weight=1)
        self.subframeButton1.columnconfigure(3, weight=1)
        self.subframeButton1.columnconfigure(4, weight=1)
        self.subframeButton2.grid_propagate(0)
        self.subframeButton2.rowconfigure(0, weight=1)
        self.subframeButton2.rowconfigure(1, weight=1)
        self.subframeButton2.columnconfigure(0, weight=1)
        self.subframeButton2.columnconfigure(1, weight=1)

        #================================
        # self.frameTop-self.frameTime
        #=================================
        # Make Label
        self.labelTime1 = tk.Label(self.frameTime, text="Exposure Time (sec)", bg=colorBrightGray, fg="white",
                                   font=fontSmallLabel)
        self.labelTime2 = tk.Label(self.frameTime, textvariable=self.exposureTime, bg=colorBrightGray, fg="white", font=fontMiddleLabel)

        # Positioning
        self.labelTime1.place(in_=self.frameTime, x=10, y=10, width=335, height=30)
        self.labelTime2.place(in_=self.frameTime, x=10, y=45, width=335, height=70)

        # Binding
        self.labelTime1.bind("<Button-1>", lambda event: self.status.OpStatusChange("TIME_INPUT"))
        self.labelTime2.bind("<Button-1>", lambda event: self.status.OpStatusChange("TIME_INPUT"))

        #================================
        # self.frameTop-self.framePower
        #================================
        self.labelPower1 = tk.Label(self.framePower, text="Power (mW/cm²)", bg=colorDarkGray, fg="white",
                                    font=fontSmallLabel)
        self.labelPower2 = tk.Label(self.framePower, textvariable=self.outputPower, bg=colorDarkGray, fg="white", font=fontMiddleLabel)

        # positioning
        self.labelPower1.place(in_=self.framePower, x=0, y=5, width=220, height=25)
        self.labelPower2.place(in_=self.framePower, x=0, y=40, width=220, height=55)

        #================================
        # self.frameTop-self.frameCurrent
        #================================
        self.labelCurrent1 = tk.Label(self.frameCurrent, text="Current (A)", bg=colorDarkGray, fg="white",
                                      font=fontSmallLabel)
        self.labelCurrent2 = tk.Label(self.frameCurrent, textvariable=self.ledCurrent, bg=colorDarkGray, fg="white",
                                      font=fontMiddleLabel)

        # positioning
        self.labelCurrent1.place(in_=self.frameCurrent, x=0, y=5, width=180, height=25)
        self.labelCurrent2.place(in_=self.frameCurrent, x=0, y=40, width=180, height=55)

        #================================
        # self.frameTop-self.frameTemper
        #================================
        self.labelTemper1 = tk.Label(self.frameTemper, text="Temperature (℃)", bg=colorDarkGray, fg="white",
                                     font=fontSmallLabel)
        self.labelTemper2 = tk.Label(self.frameTemper, textvariable=temperature, bg=colorDarkGray, fg="white", font=fontMiddleLabel)

        self.labelTemper1.place(in_=self.frameTemper, x=0, y=5, width=180, height=25)
        self.labelTemper2.place(in_=self.frameTemper, x=0, y=40, width=180, height=55)

        #=================================
        # self.frameButton - self.subframeButton1
        #=================================
        buttonNum1 = tk.Button(self.subframeButton1, highlightthickness=0, text="1", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("1"))
        buttonNum2 = tk.Button(self.subframeButton1, highlightthickness=0, text="2", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("2"))
        buttonNum3 = tk.Button(self.subframeButton1, highlightthickness=0, text="3", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("3"))
        buttonNum4 = tk.Button(self.subframeButton1, highlightthickness=0, text="4", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("4"))
        buttonNum5 = tk.Button(self.subframeButton1, highlightthickness=0, text="5", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("5"))
        buttonNum6 = tk.Button(self.subframeButton1, highlightthickness=0, text="6", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("6"))
        buttonNum7 = tk.Button(self.subframeButton1, highlightthickness=0, text="7", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("7"))
        buttonNum8 = tk.Button(self.subframeButton1, highlightthickness=0, text="8", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("8"))
        buttonNum9 = tk.Button(self.subframeButton1, highlightthickness=0, text="9", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("9"))
        buttonNum0 = tk.Button(self.subframeButton1, highlightthickness=0, text="0", bg=colorGray, fg="white",
                               font=fontMiddleLabel, width=1, activeforeground="white",
                               activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("0"))
        buttonPoint = tk.Button(self.subframeButton2, highlightthickness=0, text=".", bg=colorGray, fg="white",
                                font=fontMiddleLabel, width=1, activeforeground="white",
                                activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("point"))
        buttonClear = tk.Button(self.subframeButton2, highlightthickness=0, text="C", bg=colorGray, fg="white",
                                font=fontMiddleLabel, width=1, activeforeground="white",
                                activebackground=colorGray, command=lambda: self.callBacks.KeyInputCheck("clear"))
        buttonCancel = tk.Button(self.subframeButton2, highlightthickness=0, text="X", bg=colorRed, fg="white",
                                 font=fontMiddleLabel, width=1, activeforeground="white",
                                 activebackground=colorRed, command=lambda: self.callBacks.KeyInputCheck("cancel"))
        buttonConfirm = tk.Button(self.subframeButton2, highlightthickness=0, text="O", bg=colorGreen, fg="white",
                                  font=fontMiddleLabel, width=1, activeforeground="white",
                                  activebackground=colorGreen, command=lambda: self.callBacks.KeyInputCheck("confirm"))

        # Positioning
        buttonNum1.grid(row=0, column=0, sticky="nwes", padx=10, pady=10)
        buttonNum2.grid(row=0, column=1, sticky="nwes", padx=10, pady=10)
        buttonNum3.grid(row=0, column=2, sticky="nwes", padx=10, pady=10)
        buttonNum4.grid(row=0, column=3, sticky="nwes", padx=10, pady=10)
        buttonNum5.grid(row=0, column=4, sticky="nwes", padx=10, pady=10)
        buttonNum6.grid(row=1, column=0, sticky="nwes", padx=10, pady=10)
        buttonNum7.grid(row=1, column=1, sticky="nwes", padx=10, pady=10)
        buttonNum8.grid(row=1, column=2, sticky="nwes", padx=10, pady=10)
        buttonNum9.grid(row=1, column=3, sticky="nwes", padx=10, pady=10)
        buttonNum0.grid(row=1, column=4, sticky="nwes", padx=10, pady=10)
        buttonPoint.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        buttonClear.grid(row=0, column=1, sticky="nwes", padx=10, pady=10)
        buttonCancel.grid(row=1, column=0, sticky="nwes", padx=10, pady=10)
        buttonConfirm.grid(row=1, column=1, sticky="nwes", padx=10, pady=10)




        #==============================
        # Root-self.framePaused
        #=============================
        self.labelPausedTitle = tk.Label(self.framePaused, text="Exposure Paused", bg=colorIvory, fg="black",
                                         font=fontMiddleLabelBold2)
        self.labelPausedTimeFixed = tk.Label(self.framePaused, text="Exposed Time (sec)", bg=colorIvory, fg="black",
                                             font=fontSmallLabel2, anchor="w")
        self.labelPausedTime = tk.Label(self.framePaused, textvariable=self.elapsedTime, bg=colorIvory, fg="black",
                                        font=fontSmallLabelBold2, anchor="w")
        self.labelPausedEnergyFixed = tk.Label(self.framePaused, text="Exposed Energy (mJ/cm²)", bg=colorIvory, fg="black",
                                               font=fontSmallLabel2, anchor="w")
        self.labelPausedEnergy = tk.Label(self.framePaused, textvariable=self.elapsedEnergy, bg=colorIvory, fg="black",
                                          font=fontSmallLabelBold2, anchor="w")
        self.buttonContinue = tk.Button(self.framePaused, text="Continue", bg=colorBrightGreen, fg="white",
                                        font=fontMiddleLabel2, activeforeground="white",
                                        activebackground=colorBrightGreen, command=lambda: self.callBacks.KeyInputCheck("continue"))
        self.buttonStop = tk.Button(self.framePaused, text="Stop", bg=colorBrightRed, fg="white", font=fontMiddleLabel2,
                                    activeforeground="white", activebackground=colorBrightRed,
                                    command=lambda: self.callBacks.KeyInputCheck("stop"))

        # Positioning

        self.framePaused.place(x=83, y=85)
        self.labelPausedTitle.place(in_=self.framePaused, x=141, y=25, width=350, height=45)
        self.labelPausedTimeFixed.place(in_=self.framePaused, x=30, y=91, width=320, height=40)
        self.labelPausedTime.place(in_=self.framePaused, x=370, y=91, width=160, height=40)
        self.labelPausedEnergyFixed.place(in_=self.framePaused, x=30, y=126, width=320, height=40)
        self.labelPausedEnergy.place(in_=self.framePaused, x=370, y=126, width=160, height=40)
        self.buttonContinue.place(in_=self.framePaused, x=30, y=195, width=270, height=90)
        self.buttonStop.place(in_=self.framePaused, x=330, y=195, width=270, height=90)



        #=======================
        # Root-self.tabSetting
        #=======================


        self.frameSetting1 = tk.Frame(self.tabSetting, bg=colorDarkGray)
        self.tabSetting.add(self.frameSetting1, text="Output Power")

        self.frameSetting2 = tk.Frame(self.tabSetting, bg=colorDarkGray)
        self.tabSetting.add(self.frameSetting2, text="System Info")

        frameSetting3 = tk.Frame(self.tabSetting, bg=colorDarkGray)
        self.tabSetting.add(frameSetting3, text="Lithography")

        frameSetting4 = tk.Frame(self.tabSetting, bg=colorDarkGray)
        self.tabSetting.add(frameSetting4, text="Go Back")



        #=======================
        # self.tabSetting-self.frameSetting1
        #=======================
        self.framePowerInSetting = tk.Frame(self.frameSetting1, height=100, width=355, bg=colorDarkGray,
                                            highlightbackground="yellow", highlightthickness=2)


        #=======================
        # self.tabSetting-self.frameSetting1-self.framePowerInSetting
        #=======================
        self.labelPowerInSetting1 = tk.Label(self.framePowerInSetting, text="Power (mW/cm²)", bg=colorDarkGray, fg="white",
                                             font=fontSmallLabel)
        self.labelPowerInSetting2 = tk.Label(self.framePowerInSetting, textvariable=self.outputPower, bg=colorDarkGray, fg="yellow",
                                             font=fontMiddleLabel)

        # Positioning

        self.framePowerInSetting.place(x=230, y=40)
        self.labelPowerInSetting1.place(in_=self.framePowerInSetting, x=0, y=5, width=335, height=25)
        self.labelPowerInSetting2.place(in_=self.framePowerInSetting, x=0, y=40, width=335, height=55)


        #==========================
        # self.tabSetting-self.frameSetting2
        #==========================
        self.labelFirmwareVersion = tk.Label(self.frameSetting2, text="Software Version: CBLI-A-01-01", bg=colorDarkGray,
                                             fg="white", font=fontSmallLabelBold2)
        self.labelTotalTime = tk.Label(self.frameSetting2, text="Accumulated Exposure Time: [ 120hr,  32min, 07sec ]",
                                       bg=colorDarkGray, fg="white", font=fontSmallLabelBold2)

        # Positioning
        self.labelFirmwareVersion.place(in_=self.frameSetting2, x=30, y=100)
        self.labelTotalTime.place(in_=self.frameSetting2, x=30, y=150)


        #=======================
        # self.tabSetting-frameSetting3 (Lithography)
        #=======================

        fig = Figure(figsize=(12, 5), facecolor='white')

        axis  = fig.add_subplot(111)                  # 1 row, 1 column

        xValues  = [1,2,3,4]
        yValues0 = [6,7.5,8,7.5]
        yValues1 = [5.5,6.5,8,6]
        yValues2 = [6.5,7,8,7]

        t0, = axis.plot(xValues, yValues0, color='purple')  # change the color of the plotted line
        t1, = axis.plot(xValues, yValues1, color='red')
        t2, = axis.plot(xValues, yValues2, color='blue')

        axis.set_ylabel('Vertical Label')
        axis.set_xlabel('Horizontal Label')

        axis.grid()

        fig.legend((t0, t1, t2), ('First line', 'Second line', 'Third line'), 'upper right')
        canvas = FigureCanvasTkAgg(fig, master=frameSetting3)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        #==============================
        # Root-self.frameSplash
        #================================
        # variable
        self.cellaLogo = PhotoImage(file="../images/cella_logo.png")
        # self.cellaLogo = PhotoImage(file=self.image_path+"cella_logo.png")
        self.cellaLogo = self.cellaLogo.subsample(2, 2) #이미지 작게 만들기
        # UI component
        Splash_Logo = tk.Label(self.frameSplash, image=self.cellaLogo, bg="black")
        labelForLogo = tk.Label(self.frameSplash, text="Please touch the screen", bg="black", fg="white", font=fontSmallLabel)

        # Positioning
        Splash_Logo.place(in_=self.frameSplash, x=0, y=0, width=800, height=480)
        labelForLogo.place(in_=self.frameSplash, x=300, y=390, width=220, height=20)

        # Binding
        Splash_Logo.bind("<Button-1>", lambda event: self.status.OpStatusChange("FIRST_TOUCH"))






#======================
# Start GUI
#=======================
if __name__=="__main__":
    gui = GUI()
    gui.root.mainloop()

    print("HELLO FROM LAST SENTENCE")