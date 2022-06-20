import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage


########################################
############# UI Section ##############
######################################

#================================
# Root
#===============================
global root
root = tk.Tk()
root.wm_geometry("800x480")
root.resizable(False, False)
root.attributes('-fullscreen', True)


#================================
# Root - All Frames
#=================================

#UI Component
frameTop = tk.Frame(root, height=480, width=800, bg=common.colorDarkGray)
frameButton = tk.Frame(root, height=290, width=800, bg=common.colorDarkGray)
framePaused = tk.Frame(root, height=310, width=634, bg=common.colorIvory, highlightthickness=2,
                       highlightbackground="gray")
tabSetting = ttk.Notebook(root, width=800, height=480)
frameSplash = tk.Frame(root, height=480, width=800, bg=common.colorDarkGray)


# Positioning
frameTop.place(x=0, y=0)
frameButton.place(x=1, y=190)  ## to hide 1 pixel vertical line by tabSetting notebook widget

tabSetting.place(x=0, y=0)
frameSplash.place(x=0, y=0)

#Binding
tabSetting.bind("<<NotebookTabChanged>>", tabChanged)


#===============================
# Root - frameTop
#===============================
# Variable
tempImage = PhotoImage(file="/home/pi/Desktop/lithography/gearImage.png")
tempImage = tempImage.subsample(6, 6)

# UI component
frameTime = tk.Frame(frameTop, height=130, width=355, bg=common.colorBrightGray, highlightbackground="yellow")
frameEnergy = tk.Frame(frameTop, height=130, width=355, bg=common.colorBrightGray, highlightbackground="yellow")
labelEnergy1 = tk.Label(frameTop, text="Exposure Energy (mJ/cm²)", bg=common.colorBrightGray, fg="white",
                        font=common.fontSmallLabel)
labelEnergy2 = tk.Label(frameTop, text=exposureEnergy, bg=common.colorBrightGray, fg="white",
                        font=common.fontMiddleLabel)
framePower = tk.Frame(frameTop, height=100, width=220, bg=common.colorDarkGray)
frameCurrent = tk.Frame(frameTop, height=100, width=180, bg=common.colorDarkGray)
frameTemper = tk.Frame(frameTop, height=100, width=180, bg=common.colorDarkGray)
buttonStartStop = tk.Button(frameTop, highlightthickness=0, text="START", bg=common.colorGreen, fg="white",
                            font=common.fontLargeLabel, activeforeground="white", activebackground=common.colorGreen,
                            command=lambda: KeyInputCheck("startStop"))
buttonSetting = tk.Button(frameTop, highlightthickness=0, image=tempImage, command=lambda: KeyInputCheck("setting"))
labelSensor1 = tk.Label(frameTop, text="Sensor Value: ", bg=common.colorDarkGray, fg="white",
                        font=common.fontSmallLabel)
labelSensor2 = tk.Label(frameTop, text="0", bg=common.colorDarkGray, fg="white", font=common.fontSmallLabel)
labelExit = tk.Label(frameTop, bg=common.colorDarkGray)


# Positioning
frameTime.place(x=30, y=30, height=130, width=355)
labelTime1.place(in_=frameTime, x=10, y=10, width=335, height=30)
labelTime2.place(in_=frameTime, x=10, y=45, width=335, height=70)

frameEnergy.place(x=415, y=30)
labelEnergy1.place(in_=frameEnergy, x=10, y=10, width=335, height=30)
labelEnergy2.place(in_=frameEnergy, x=10, y=45, width=335, height=70)

framePower.place(x=30, y=350)
labelPower1.place(in_=framePower, x=0, y=5, width=220, height=25)
labelPower2.place(in_=framePower, x=0, y=40, width=220, height=55)

frameCurrent.place(x=270, y=350)
labelCurrent1.place(in_=frameCurrent, x=0, y=5, width=180, height=25)
labelCurrent2.place(in_=frameCurrent, x=0, y=40, width=180, height=55)

frameTemper.place(x=470, y=350)
labelTemper1.place(in_=frameTemper, x=0, y=5, width=180, height=25)
labelTemper2.place(in_=frameTemper, x=0, y=40, width=180, height=55)

buttonStartStop.place(x=30, y=190, width=740, height=130)
buttonSetting.place(x=670, y=350, width=100, height=100)

labelSensor1.place(in_=frameTop, x=30, y=7, width=120, height=18)
labelSensor2.place(in_=frameTop, x=150, y=7, width=150, height=18)

labelExit.place(in_=frameTop, x=700, y=0, width=100, height=18)

# Binding
frameTime.bind("<Button-1>", lambda event: OpStatusChange("TIME_INPUT"))
frameEnergy.bind("<Button-1>", lambda event: OpStatusChange("ENERGY_INPUT"))
labelEnergy1.bind("<Button-1>", lambda event: OpStatusChange("ENERGY_INPUT"))
labelEnergy2.bind("<Button-1>", lambda event: OpStatusChange("ENERGY_INPUT"))

labelExit.bind("<Button-1>", lambda event: OpStatusChange("EXIT"))

#==============================
# Root - frameButton
#==============================
subframeButton1 = tk.Frame(frameButton, height=210, width=525, bg=common.colorDarkGray)
subframeButton2 = tk.Frame(frameButton, height=210, width=210, bg=common.colorDarkGray)

subframeButton1.place(in_=frameButton, x=20, y=25)
subframeButton2.place(in_=frameButton, x=570, y=25)

# Positioning
subframeButton1.grid_propagate(0)
subframeButton1.rowconfigure(0, weight=1)
subframeButton1.rowconfigure(1, weight=1)
subframeButton1.columnconfigure(0, weight=1)
subframeButton1.columnconfigure(1, weight=1)
subframeButton1.columnconfigure(2, weight=1)
subframeButton1.columnconfigure(3, weight=1)
subframeButton1.columnconfigure(4, weight=1)
subframeButton2.grid_propagate(0)
subframeButton2.rowconfigure(0, weight=1)
subframeButton2.rowconfigure(1, weight=1)
subframeButton2.columnconfigure(0, weight=1)
subframeButton2.columnconfigure(1, weight=1)

#================================
# frameTop-frameTime
#=================================
# Make Label
labelTime1 = tk.Label(frameTime, text="Exposure Time (sec)", bg=common.colorBrightGray, fg="white",
                      font=common.fontSmallLabel)
labelTime2 = tk.Label(frameTime, text=exposureTime, bg=common.colorBrightGray, fg="white", font=common.fontMiddleLabel)

# Binding
labelTime1.bind("<Button-1>", lambda event: OpStatusChange("TIME_INPUT"))
labelTime2.bind("<Button-1>", lambda event: OpStatusChange("TIME_INPUT"))

#================================
# frameTop-framePower
#================================
labelPower1 = tk.Label(framePower, text="Power (mW/cm²)", bg=common.colorDarkGray, fg="white",
                       font=common.fontSmallLabel)
labelPower2 = tk.Label(framePower, text=outputPower, bg=common.colorDarkGray, fg="white", font=common.fontMiddleLabel)

#================================
# frameTop-frameCurrent
#================================
labelCurrent1 = tk.Label(frameCurrent, text="Current (A)", bg=common.colorDarkGray, fg="white",
                         font=common.fontSmallLabel)
labelCurrent2 = tk.Label(frameCurrent, text=ledCurrent, bg=common.colorDarkGray, fg="white",
                         font=common.fontMiddleLabel)

#================================
# frameTop-frameTemper
#================================
labelTemper1 = tk.Label(frameTemper, text="Temperature (℃)", bg=common.colorDarkGray, fg="white",
                        font=common.fontSmallLabel)
labelTemper2 = tk.Label(frameTemper, text=temperature, bg=common.colorDarkGray, fg="white", font=common.fontMiddleLabel)


#=================================
# frameButton - subframeButton1
#=================================
buttonNum1 = tk.Button(subframeButton1, highlightthickness=0, text="1", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("1"))
buttonNum2 = tk.Button(subframeButton1, highlightthickness=0, text="2", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("2"))
buttonNum3 = tk.Button(subframeButton1, highlightthickness=0, text="3", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("3"))
buttonNum4 = tk.Button(subframeButton1, highlightthickness=0, text="4", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("4"))
buttonNum5 = tk.Button(subframeButton1, highlightthickness=0, text="5", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("5"))
buttonNum6 = tk.Button(subframeButton1, highlightthickness=0, text="6", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("6"))
buttonNum7 = tk.Button(subframeButton1, highlightthickness=0, text="7", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("7"))
buttonNum8 = tk.Button(subframeButton1, highlightthickness=0, text="8", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("8"))
buttonNum9 = tk.Button(subframeButton1, highlightthickness=0, text="9", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("9"))
buttonNum0 = tk.Button(subframeButton1, highlightthickness=0, text="0", bg=common.colorGray, fg="white",
                       font=common.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=common.colorGray, command=lambda: KeyInputCheck("0"))
buttonPoint = tk.Button(subframeButton2, highlightthickness=0, text=".", bg=common.colorGray, fg="white",
                        font=common.fontMiddleLabel, width=1, activeforeground="white",
                        activebackground=common.colorGray, command=lambda: KeyInputCheck("point"))
buttonClear = tk.Button(subframeButton2, highlightthickness=0, text="C", bg=common.colorGray, fg="white",
                        font=common.fontMiddleLabel, width=1, activeforeground="white",
                        activebackground=common.colorGray, command=lambda: KeyInputCheck("clear"))
buttonCancel = tk.Button(subframeButton2, highlightthickness=0, text="X", bg=common.colorRed, fg="white",
                         font=common.fontMiddleLabel, width=1, activeforeground="white",
                         activebackground=common.colorRed, command=lambda: KeyInputCheck("cancel"))
buttonConfirm = tk.Button(subframeButton2, highlightthickness=0, text="O", bg=common.colorGreen, fg="white",
                          font=common.fontMiddleLabel, width=1, activeforeground="white",
                          activebackground=common.colorGreen, command=lambda: KeyInputCheck("confirm"))

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
# Root-framePaused
#=============================
labelPausedTitle = tk.Label(framePaused, text="Exposure Paused", bg=common.colorIvory, fg="black",
                            font=common.fontMiddleLabelBold2)
labelPausedTimeFixed = tk.Label(framePaused, text="Exposed Time (sec)", bg=common.colorIvory, fg="black",
                                font=common.fontSmallLabel2, anchor="w")
labelPausedTime = tk.Label(framePaused, text=str(elapsedTime), bg=common.colorIvory, fg="black",
                           font=common.fontSmallLabelBold2, anchor="w")
labelPausedEnergyFixed = tk.Label(framePaused, text="Exposed Energy (mJ/cm²)", bg=common.colorIvory, fg="black",
                                  font=common.fontSmallLabel2, anchor="w")
labelPausedEnergy = tk.Label(framePaused, text=str(elapsedTime * outputPower), bg=common.colorIvory, fg="black",
                             font=common.fontSmallLabelBold2, anchor="w")
buttonContinue = tk.Button(framePaused, text="Continue", bg=common.colorBrightGreen, fg="white",
                           font=common.fontMiddleLabel2, activeforeground="white",
                           activebackground=common.colorBrightGreen, command=lambda: KeyInputCheck("continue"))
buttonStop = tk.Button(framePaused, text="Stop", bg=common.colorBrightRed, fg="white", font=common.fontMiddleLabel2,
                       activeforeground="white", activebackground=common.colorBrightRed,
                       command=lambda: KeyInputCheck("stop"))

# Positioning

framePaused.place(x=83, y=85)
labelPausedTitle.place(in_=framePaused, x=141, y=25, width=350, height=45)
labelPausedTimeFixed.place(in_=framePaused, x=30, y=91, width=320, height=40)
labelPausedTime.place(in_=framePaused, x=370, y=91, width=160, height=40)
labelPausedEnergyFixed.place(in_=framePaused, x=30, y=126, width=320, height=40)
labelPausedEnergy.place(in_=framePaused, x=370, y=126, width=160, height=40)
buttonContinue.place(in_=framePaused, x=30, y=195, width=270, height=90)
buttonStop.place(in_=framePaused, x=330, y=195, width=270, height=90)



#=======================
# Root-tabSetting
#=======================
frameSetting1 = tk.Frame(tabSetting, bg=common.colorDarkGray)
tabSetting.add(frameSetting1, text="Output Power")

frameSetting2 = tk.Frame(tabSetting, bg=common.colorDarkGray)
tabSetting.add(frameSetting2, text="System Info")


#=======================
# tabSetting-frameSetting1
#=======================
framePowerInSetting = tk.Frame(frameSetting1, height=100, width=355, bg=common.colorDarkGray,
                               highlightbackground="yellow", highlightthickness=2)


#=======================
# tabSetting-frameSetting1-framePowerInSetting
#=======================
labelPowerInSetting1 = tk.Label(framePowerInSetting, text="Power (mW/cm²)", bg=common.colorDarkGray, fg="white",
                                font=common.fontSmallLabel)
labelPowerInSetting2 = tk.Label(framePowerInSetting, text=outputPower, bg=common.colorDarkGray, fg="yellow",
                                font=common.fontMiddleLabel)

# Positioning

framePowerInSetting.place(x=230, y=40)
labelPowerInSetting1.place(in_=framePowerInSetting, x=0, y=5, width=335, height=25)
labelPowerInSetting2.place(in_=framePowerInSetting, x=0, y=40, width=335, height=55)


#==========================
# tabSetting-frameSetting2
#==========================
labelFirmwareVersion = tk.Label(frameSetting2, text="Software Version: CBLI-A-01-01", bg=common.colorDarkGray,
                                fg="white", font=common.fontSmallLabelBold2)
labelTotalTime = tk.Label(frameSetting2, text="Accumulated Exposure Time: [ 120hr,  32min, 07sec ]",
                          bg=common.colorDarkGray, fg="white", font=common.fontSmallLabelBold2)

# Positioning
labelFirmwareVersion.place(in_=frameSetting2, x=30, y=100)
labelTotalTime.place(in_=frameSetting2, x=30, y=150)



#==============================
# Root-frameSplash
#================================
# variable
tempImage2 = PhotoImage(file="/home/pi/Desktop/lithography/cella_logo.png")
tempImage2 = tempImage2.subsample(2, 2)

# UI component
labelForLogo = tk.Label(frameSplash, image=tempImage2, bg="black")
labelForLogo = tk.Label(frameSplash, text="Please touch the screen", bg="black", fg="white", font=common.fontSmallLabel)

# Positioning
labelForLogo.place(in_=frameSplash, x=0, y=0, width=800, height=480)
labelForLogo.place(in_=frameSplash, x=300, y=390, width=220, height=20)

# Binding
labelForLogo.bind("<Button-1>", lambda event: OpStatusChange("FIRST_TOUCH"))




#========================
# Style
#========================
style = ttk.Style()
style.theme_create("customTabStyle", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
    "TNotebook.Tab": {
        "configure": {"padding": [20, 10], "background": common.colorBrightGray, "foreground": "white",
                      "font": ('family Calibri', '12', 'bold')},
        "map": {"background": [("selected", common.colorDarkGray)],
                "expand": [("selected", [1, 1, 1, 0])]}}})

style.theme_use("customTabStyle")



# frameTop.lift()
frameSplash.lift()

#======================
# Start GUI
#=======================
root.mainloop()

######## references
##       btnFrame.place_forget()
