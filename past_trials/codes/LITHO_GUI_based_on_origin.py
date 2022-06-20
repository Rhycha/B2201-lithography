from LITHO_package import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
import enum
import threading
# import serial #circuitpython 설치해야 module 지원
import sys
import random
from os import path
from time import sleep
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from develop.model import exposureTime, elapsedTime, exposureEnergy

fDir    = path.dirname(__file__)
exposureTime = 12.0 # Predetermined value
elapsedTime = 0.0 # Measured valued after start
exposureEnergy = 240.0
outputIntensity = 20.0
ledCurrent = 0
temperature = 42
firstEntered = True
sensorValue = 0
stop_logging_thread = False


class OpStatus(enum.Enum):
    READY = 0
    TIME_INPUT = 1
    ENERGY_INPUT = 2
    EXPOSURE = 3
    PAUSED = 4
    SETTING = 5


class AsyncTask:
    def __init__(self):
        pass

    def exposureTask(self):
        global elapsedTime
        ##        print ('Exposure Task is running')    ## print generate large delay during timer run
        if (opStatus == OpStatus.EXPOSURE):
            exposure_thread = threading.Timer(0.1, self.exposureTask)
            exposure_thread.setDaemon(True) #강제종료 했을 때 Thread 종료되게
            exposure_thread.start()
            # exposuretime 이만큼 실행시키겠다. (ex : ~10초까지만)
            if round(elapsedTime, 1) < round(exposureTime, 1):
                if elapsedTime == 0:
                    pass
                else:

                    ledCurrent = random.uniform(0, 5)
                    tempString = str(round(ledCurrent, 1))
                    labelCurrent2.configure(text=tempString)

                    sensorValue = random.uniform(1,9)
                    tempString = str(sensorValue)
                    labelSensor2.configure(text=tempString)

                elapsedTime += 0.1
                tempString = str(round(elapsedTime, 1)) + '/' + str(exposureTime)
                labelTime2.configure(text=tempString)
                tempString = str(round(elapsedTime * outputIntensity, 1)) + '/' + str(exposureEnergy)
                labelEnergy2.configure(text=tempString)




            else:
                labelTime2.configure(text=str(exposureTime))
                labelEnergy2.configure(text=str(exposureEnergy))
                elapsedTime = 0

                labelCurrent2.configure(text="0")
                OpStatusChange("READY")


at = AsyncTask()
opStatus = OpStatus.READY


def testFunction(event):
    print("testFuction Called")


def tabChanged(event):
    selectedTab = event.widget.select()
    tabText = event.widget.tab(selectedTab, "text")

    if tabText == "Output Intensity" and opStatus == OpStatus.SETTING:
        frameButton.lift() #Intensity input 넣기 위한 Keyboard 생성
    elif tabText == "System Info" and opStatus == OpStatus.SETTING:
        tabSetting.lift()
    elif tabText == "Lithography" and opStatus == OpStatus.SETTING:
        frameButton.lower()
    elif tabText == "Go Back" and opStatus == OpStatus.SETTING:
        frameButton.lower()
        KeyInputCheck("cancel")

def OpStatusChange(string):
    global opStatus
    global firstEntered

    if string == "READY":
        frameTime.configure(highlightthickness="0")
        frameEnergy.configure(highlightthickness="0")
        labelTime2.configure(text=str(exposureTime))
        labelEnergy2.configure(text=str(exposureEnergy))
        labelTime2.configure(fg="white")
        labelEnergy2.configure(fg="white")

        if opStatus == OpStatus.EXPOSURE or opStatus == OpStatus.PAUSED:
            buttonStartStop.configure(bg=LITHO_Design.colorGreen, activebackground=LITHO_Design.colorGreen, text="START")

        firstEntered = True
        opStatus = OpStatus.READY
        frameTop.lift()
        print("OpStatus: READY")


    elif (string == "TIME_INPUT"):
        if opStatus == OpStatus.READY or opStatus == OpStatus.ENERGY_INPUT:

            if opStatus == OpStatus.ENERGY_INPUT:
                tempNumber = round(float(labelEnergy2.cget('text')), 1)
                labelEnergy2.configure(text=str(tempNumber))

            opStatus = OpStatus.TIME_INPUT
            frameTime.configure(highlightthickness="2")
            frameEnergy.configure(highlightthickness="0")
            labelTime2.configure(fg="yellow")
            labelEnergy2.configure(fg="white")
            frameButton.lift()
            print("OpStatus: TIME_INPUT")

    elif string == "ENERGY_INPUT":
        if opStatus == OpStatus.READY or opStatus == OpStatus.TIME_INPUT:

            if opStatus == OpStatus.TIME_INPUT:
                tempNumber = round(float(labelTime2.cget('text')), 1)
                labelTime2.configure(text=str(tempNumber))

            frameTime.configure(highlightthickness="0")
            frameEnergy.configure(highlightthickness="2")
            labelTime2.configure(fg="white")
            labelEnergy2.configure(fg="yellow")
            opStatus = OpStatus.ENERGY_INPUT
            frameButton.lift()
            print("OpStatus: ENERGY_INPUT")

    elif string == "EXPOSURE":
        if opStatus == OpStatus.READY:
            buttonStartStop.configure(bg=LITHO_Design.colorRed, activebackground=LITHO_Design.colorRed, text="STOP")
            opStatus = OpStatus.EXPOSURE
            at.exposureTask()

        if opStatus == OpStatus.PAUSED:
            opStatus = OpStatus.EXPOSURE
            at.exposureTask()

        print("OpStatus: EXPOSURE")

    elif string == "PAUSED":
        if opStatus == OpStatus.EXPOSURE:
            opStatus = OpStatus.PAUSED

            labelPausedTime.configure(text=str(round(elapsedTime, 1)))
            labelPausedEnergy.configure(text=str(round(elapsedTime * outputIntensity, 1)))
            framePaused.lift()
            print("OpStatus: PAUSED")

    elif string == "SETTING":
        if opStatus == OpStatus.READY:
            opStatus = OpStatus.SETTING
            tabSetting.lift()
            tabSetting.select(0)
            frameButton.lift()
            print("OpStatus: SETTING")

    elif string == "FIRST_TOUCH":
        frameTop.lift()
        print("Start Thread")
        thread_temperature()

    elif string == "EXIT":
        root.destroy()
        sys.exit()


def KeyInputCheck(string):
    global firstEntered
    global exposureTime
    global exposureEnergy
    global outputIntensity
    global elapsedTime
    global stop_logging_thread


    if opStatus == OpStatus.TIME_INPUT or opStatus == OpStatus.ENERGY_INPUT:

        if string == "cancel":
            OpStatusChange("READY")
        elif string == "confirm":
            tempTime = round(float(labelTime2.cget('text')), 1)
            print("line209",tempTime)
            tempEnergy = round(tempTime * outputIntensity, 1)
            print("line211", tempEnergy)
            if tempEnergy> 4000 or tempEnergy < 100:
                frameWarning.lift() # frameWarning에서 deny를 누르면 아무 동작 안함.
                frameWarning.grab_set()
            else:
                exposureTime = tempTime
                exposureEnergy = tempEnergy
                OpStatusChange("READY")
        else:
            if opStatus == OpStatus.TIME_INPUT:
                if string == "point":
                    tempString = str(labelTime2.cget('text'))
                    if '.' not in tempString:
                        labelTime2.configure(text=tempString + '.')

                elif string == "clear":
                    tempNumber = 0
                    labelTime2.configure(text=str(tempNumber))
                    labelEnergy2.configure(text=str(tempNumber * outputIntensity))

                else:
                    if firstEntered == False:
                        if float(labelTime2.cget('text')) != 0:
                            tempNumber = round(100 * float(labelTime2.cget('text')))
                            tempNumber = tempNumber % 10
                            if tempNumber == 0:
                                tempString = str(labelTime2.cget('text')) + string
                            else:
                                tempString = str(labelTime2.cget('text'))

                            tempNumber = round(float(tempString), 1)
                            if tempNumber > 600:
                                tempNumber = 600
                                labelTime2.configure(text=str(tempNumber))
                            else:
                                labelTime2.configure(text=tempString)
                        else:
                            tempNumber = int(string)
                            labelTime2.configure(text=string)

                    elif firstEntered == True:
                        tempNumber = int(string)
                        labelTime2.configure(text=string)
                        firstEntered = False

                    tempNumber = float(round(tempNumber * outputIntensity, 1))
                    labelEnergy2.configure(text=str(tempNumber))


            elif opStatus == OpStatus.ENERGY_INPUT:
                if string == "point":
                    tempString = str(labelEnergy2.cget('text'))
                    if '.' not in tempString:
                        labelEnergy2.configure(text=tempString + '.')

                elif string == "clear":
                    tempNumber = 0
                    labelTime2.configure(text=str(tempNumber))
                    labelEnergy2.configure(text=str(tempNumber * outputIntensity))

                else:
                    if firstEntered == False:
                        if float(labelEnergy2.cget('text')) != 0:
                            tempNumber = round(100 * float(labelEnergy2.cget('text')))
                            tempNumber = tempNumber % 10
                            if tempNumber == 0:
                                tempString = str(labelEnergy2.cget('text')) + string
                            else:
                                tempString = str(labelEnergy2.cget('text'))

                            tempNumber = round(float(tempString), 1)
                            if tempNumber > 600 * outputIntensity:
                                tempNumber = 600 * outputIntensity
                                labelEnergy2.configure(text=str(tempNumber))
                            else:
                                labelEnergy2.configure(text=tempString)
                        else:
                            tempNumber = int(string)
                            labelEnergy2.configure(text=string)

                    elif firstEntered == True:
                        tempNumber = int(string)
                        labelEnergy2.configure(text=string)
                        firstEntered = False

                    tempNumber = float(round(tempNumber / outputIntensity, 1))
                    labelTime2.configure(text=str(tempNumber))


    elif opStatus == OpStatus.READY:
        if string == "startStop":
            OpStatusChange("EXPOSURE")
            stop_logging_thread = False #flag 변경 후
            create_logging_thread() #Thread 시작

        if string == "setting":
            OpStatusChange("SETTING")

    elif opStatus == OpStatus.EXPOSURE:
        if string == "startStop":
            stop_logging_thread = True #log 기록 정지
            buttonStartStop.configure(state=tk.DISABLED)
            OpStatusChange("PAUSED")
            labelCurrent2.configure(text="0")


    elif opStatus == OpStatus.PAUSED:
        if string == "continue":
            frameTop.lift()
            buttonStartStop.configure(state=tk.NORMAL)
            OpStatusChange("EXPOSURE")
            stop_logging_thread = False #flag를 다시 변경하고
            create_logging_thread() #log 기록 재시작


        if string == "stop":
            buttonStartStop.configure(state=tk.NORMAL)
            elapsedTime = 0.0
            OpStatusChange("READY")

    elif opStatus == OpStatus.SETTING:
        if string == "cancel":
            OpStatusChange("READY")
        elif string == "confirm":
            outputIntensity = round(float(labelIntensityInSetting2.cget('text')), 1)
            exposureEnergy = round(exposureTime * outputIntensity, 1)
            OpStatusChange("READY")
            labelIntensity2.configure(text=str(outputIntensity))

        else:
            if string == "point":
                tempString = str(labelIntensityInSetting2.cget('text'))
                if '.' not in tempString:
                    labelIntensityInSetting2.configure(text=tempString + '.')

            elif string == "clear":
                tempNumber = 0
                labelIntensityInSetting2.configure(text=str(tempNumber))
                labelEnergy2.configure(text=str(tempNumber * outputIntensity))

            else:
                if firstEntered == False:
                    if float(labelIntensityInSetting2.cget('text')) != 0:
                        tempNumber = round(100 * float(labelIntensityInSetting2.cget('text')))
                        tempNumber = tempNumber % 10
                        if tempNumber == 0:
                            tempString = str(labelIntensityInSetting2.cget('text')) + string
                        else:
                            tempString = str(labelIntensityInSetting2.cget('text'))

                        tempNumber = round(float(tempString), 1)
                        labelIntensityInSetting2.configure(text=tempString)

                    else:
                        tempNumber = int(string)
                        labelIntensityInSetting2.configure(text=string)

                elif firstEntered == True:
                    tempNumber = int(string)
                    labelIntensityInSetting2.configure(text=string)
                    firstEntered = False

                tempNumber = float(round(tempNumber * exposureTime, 1))
                labelEnergy2.configure(text=str(tempNumber))



def logging():
    global stop_logging_thread
    sleep(0.1)
    print("Hello, world!")
    while 1:
        if stop_logging_thread:
            break
        sleep(1)
        print("Hello, world!")


def create_logging_thread():
    logging_thread= threading.Thread(target=logging)
    logging_thread.setDaemon(True)
    logging_thread.start()


def read_temperature():
    global temperature
    global gui_temperature
    while 1:
        sleep(1)
        print("read_temperature",datetime.datetime.now())
        temperature = random.randint(10, 60)
        gui_temperature.set(temperature)

def read_temperature2():
    while 1:
        sleep(1)
        print("read_temperature")

def thread_temperature():
    global temperature
    temperature_thread = threading.Thread(target=read_temperature)
    temperature_thread.setDaemon(True)
    temperature_thread.start()


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


# def _quit():
#     root.quit()
#     root.destroy()
#     exit()

#================================
# Root - All Frames
#=================================

#UI Component
frameTop = tk.Frame(root, height=480, width=800, bg=LITHO_Design.colorDarkGray)
frameButton = tk.Frame(root, height=290, width=800, bg=LITHO_Design.colorDarkGray)
framePaused = tk.Frame(root, height=310, width=634, bg=LITHO_Design.colorIvory, highlightthickness=2,
                       highlightbackground="gray")
tabSetting = ttk.Notebook(root, width=800, height=480)
frameSplash = tk.Frame(root, height=480, width=800, bg=LITHO_Design.colorDarkGray)
frameWarning = tk.Frame(root, height=200, width=400, bg=LITHO_Design.colorDarkGray,
                        padx=30, pady=10, borderwidth=5, relief="raised")


# Positioning
frameTop.place(x=0, y=0)
frameButton.place(x=1, y=190)  ## to hide 1 pixel vertical line by tabSetting notebook widget

tabSetting.place(x=0, y=0)
frameSplash.place(x=0, y=0)
frameWarning.place(x=30, y=100)

#Binding
tabSetting.bind("<<NotebookTabChanged>>", tabChanged)


#===============================
# Root - frameTop
#===============================
# Variable
tempImage = PhotoImage(file="../images/gearImageGraywithbg.png")
tempImage = tempImage.subsample(3, 3)
# tempImage = tempImage.subsample(6, 6)

# UI component
frameTime = tk.Frame(frameTop, height=130, width=355, bg=LITHO_Design.colorBrightGray, highlightbackground="yellow")
frameEnergy = tk.Frame(frameTop, height=130, width=355, bg=LITHO_Design.colorBrightGray, highlightbackground="yellow")
frameIntensity = tk.Frame(frameTop, height=100, width=220, bg=LITHO_Design.colorDarkGray)
frameCurrent = tk.Frame(frameTop, height=100, width=180, bg=LITHO_Design.colorDarkGray)
frameTemper = tk.Frame(frameTop, height=100, width=180, bg=LITHO_Design.colorDarkGray)
buttonStartStop = tk.Button(frameTop, highlightthickness=0, text="START", bg=LITHO_Design.colorGreen, fg="white",
                            font=LITHO_Design.fontLargeLabel, activeforeground="white", activebackground=LITHO_Design.colorGreen,
                            command=lambda: KeyInputCheck("startStop"))
buttonSetting = tk.Button(frameTop, highlightthickness=0, relief=tk.RAISED, image=tempImage, bg=LITHO_Design.colorDarkGray, command=lambda: KeyInputCheck("setting"))
labelSensor1 = tk.Label(frameTop, text="Sensor Value: ", bg=LITHO_Design.colorDarkGray, fg="white",
                        font=LITHO_Design.fontSmallLabel)
labelSensor2 = tk.Label(frameTop, text="0", bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontSmallLabel)
labelExit = tk.Label(frameTop, bg=LITHO_Design.colorDarkGray)


# Positioning
frameTime.place(x=30, y=30, height=130, width=355)

frameEnergy.place(x=415, y=30)

frameIntensity.place(x=30, y=350)


frameCurrent.place(x=270, y=350)


frameTemper.place(x=470, y=350)


buttonStartStop.place(x=30, y=190, width=740, height=130)
buttonSetting.place(x=670, y=350, width=100, height=100)

# labelSensor1.place(in_=frameTop, x=30, y=7, width=120, height=18)
# labelSensor2.place(in_=frameTop, x=150, y=7, width=150, height=18)

labelExit.place(in_=frameTop, x=700, y=0, width=100, height=18)

# Binding
frameTime.bind("<Button-1>", lambda event: OpStatusChange("TIME_INPUT"))
frameEnergy.bind("<Button-1>", lambda event: OpStatusChange("ENERGY_INPUT"))

labelExit.bind("<Button-1>", lambda event: OpStatusChange("EXIT"))

#==============================
# Root - frameButton
#==============================
subframeButton1 = tk.Frame(frameButton, height=210, width=525, bg=LITHO_Design.colorDarkGray)
subframeButton2 = tk.Frame(frameButton, height=210, width=210, bg=LITHO_Design.colorDarkGray)

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
labelTime1 = tk.Label(frameTime, text="Exposure Time (sec)", bg=LITHO_Design.colorBrightGray, fg="white",
                      font=LITHO_Design.fontSmallLabel)
labelTime2 = tk.Label(frameTime, text=exposureTime, bg=LITHO_Design.colorBrightGray, fg="white", font=LITHO_Design.fontMiddleLabel)
labelTimeInfo = tk.Label(frameTime, text="Qualified level: 6 ~ 50", bg=LITHO_Design.colorBrightGray, fg="white", font=LITHO_Design.fontSmallLabel)

# Positioning
labelTime1.place(in_=frameTime, x=10, y=10, width=335, height=30)
labelTime2.place(in_=frameTime, x=10, y=35, width=335, height=70)
labelTimeInfo.place(in_=frameTime, x=10, y=95, width=335, height=30)

# Binding
labelTime1.bind("<Button-1>", lambda event: OpStatusChange("TIME_INPUT"))
labelTime2.bind("<Button-1>", lambda event: OpStatusChange("TIME_INPUT"))

#================================
# frameTop-frameEnergy
#================================

labelEnergy1 = tk.Label(frameEnergy, text="Exposure Energy (mJ/cm²)", bg=LITHO_Design.colorBrightGray, fg="white",
                        font=LITHO_Design.fontSmallLabel)
labelEnergy2 = tk.Label(frameEnergy, text=exposureEnergy, bg=LITHO_Design.colorBrightGray, fg="white",
                        font=LITHO_Design.fontMiddleLabel)
labelEnergyInfo = tk.Label(frameEnergy, text="Qualified level: 100 ~ 4000", bg=LITHO_Design.colorBrightGray, fg="white", font=LITHO_Design.fontSmallLabel)


labelEnergy1.place(in_=frameEnergy, x=10, y=10, width=335, height=30)
labelEnergy2.place(in_=frameEnergy, x=10, y=35, width=335, height=70)
labelEnergyInfo.place(in_=frameEnergy, x=10, y=95, width=335, height=30)

labelEnergy1.bind("<Button-1>", lambda event: OpStatusChange("ENERGY_INPUT"))
labelEnergy2.bind("<Button-1>", lambda event: OpStatusChange("ENERGY_INPUT"))


#================================
# frameTop-frameIntensity
#================================
labelIntensity1 = tk.Label(frameIntensity, text="Intensity (mW/cm²)", bg=LITHO_Design.colorDarkGray, fg="white",
                       font=LITHO_Design.fontSmallLabel)
labelIntensity2 = tk.Label(frameIntensity, text=outputIntensity, bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontMiddleLabel)

# positioning
# labelIntensity1.place(in_=frameIntensity, x=10, y=10, width=335, height=30)
labelIntensity1.place(in_=frameIntensity, x=0, y=5, width=220, height=25)
# labelIntensity2.place(in_=frameIntensity, x=10, y=35, width=335, height=70)
labelIntensity2.place(in_=frameIntensity, x=0, y=40, width=220, height=55)

#================================
# frameTop-frameCurrent
#================================
labelCurrent1 = tk.Label(frameCurrent, text="Current (A)", bg=LITHO_Design.colorDarkGray, fg="white",
                         font=LITHO_Design.fontSmallLabel)
labelCurrent2 = tk.Label(frameCurrent, text=ledCurrent, bg=LITHO_Design.colorDarkGray, fg="white",
                         font=LITHO_Design.fontMiddleLabel)

# positioning
labelCurrent1.place(in_=frameCurrent, x=0, y=5, width=180, height=25)
labelCurrent2.place(in_=frameCurrent, x=0, y=40, width=180, height=55)

#================================
# frameTop-frameTemper
#================================
labelTemper1 = tk.Label(frameTemper, text="Temperature (℃)", bg=LITHO_Design.colorDarkGray, fg="white",
                        font=LITHO_Design.fontSmallLabel)
# labelTemper2 = tk.Label(frameTemper, text=temperature, bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontMiddleLabel)
global gui_temperature
gui_temperature = tk.IntVar()
labelTemper2 = tk.Label(frameTemper, textvariable=gui_temperature, bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontMiddleLabel)


labelTemper1.place(in_=frameTemper, x=0, y=5, width=180, height=25)
labelTemper2.place(in_=frameTemper, x=0, y=40, width=180, height=55)

#=================================
# frameButton - subframeButton1
#=================================
buttonNum1 = tk.Button(subframeButton1, highlightthickness=0, text="1", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("1"))
buttonNum2 = tk.Button(subframeButton1, highlightthickness=0, text="2", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("2"))
buttonNum3 = tk.Button(subframeButton1, highlightthickness=0, text="3", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("3"))
buttonNum4 = tk.Button(subframeButton1, highlightthickness=0, text="4", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("4"))
buttonNum5 = tk.Button(subframeButton1, highlightthickness=0, text="5", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("5"))
buttonNum6 = tk.Button(subframeButton1, highlightthickness=0, text="6", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("6"))
buttonNum7 = tk.Button(subframeButton1, highlightthickness=0, text="7", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("7"))
buttonNum8 = tk.Button(subframeButton1, highlightthickness=0, text="8", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("8"))
buttonNum9 = tk.Button(subframeButton1, highlightthickness=0, text="9", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("9"))
buttonNum0 = tk.Button(subframeButton1, highlightthickness=0, text="0", bg=LITHO_Design.colorGray, fg="white",
                       font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                       activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("0"))
buttonPoint = tk.Button(subframeButton2, highlightthickness=0, text=".", bg=LITHO_Design.colorGray, fg="white",
                        font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                        activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("point"))
buttonClear = tk.Button(subframeButton2, highlightthickness=0, text="C", bg=LITHO_Design.colorGray, fg="white",
                        font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                        activebackground=LITHO_Design.colorGray, command=lambda: KeyInputCheck("clear"))
buttonCancel = tk.Button(subframeButton2, highlightthickness=0, text="X", bg=LITHO_Design.colorRed, fg="white",
                         font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                         activebackground=LITHO_Design.colorRed, command=lambda: KeyInputCheck("cancel"))
buttonConfirm = tk.Button(subframeButton2, highlightthickness=0, text="O", bg=LITHO_Design.colorGreen, fg="white",
                          font=LITHO_Design.fontMiddleLabel, width=1, activeforeground="white",
                          activebackground=LITHO_Design.colorGreen, command=lambda: KeyInputCheck("confirm"))

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
labelPausedTitle = tk.Label(framePaused, text="Exposure Paused", bg=LITHO_Design.colorIvory, fg="black",
                            font=LITHO_Design.fontMiddleLabelBold2)
labelPausedTimeFixed = tk.Label(framePaused, text="Exposed Time (sec)", bg=LITHO_Design.colorIvory, fg="black",
                                font=LITHO_Design.fontSmallLabel2, anchor="w")
labelPausedTime = tk.Label(framePaused, text=str(elapsedTime), bg=LITHO_Design.colorIvory, fg="black",
                           font=LITHO_Design.fontSmallLabelBold2, anchor="w")
labelPausedEnergyFixed = tk.Label(framePaused, text="Exposed Energy (mJ/cm²)", bg=LITHO_Design.colorIvory, fg="black",
                                  font=LITHO_Design.fontSmallLabel2, anchor="w")
labelPausedEnergy = tk.Label(framePaused, text=str(elapsedTime * outputIntensity), bg=LITHO_Design.colorIvory, fg="black",
                             font=LITHO_Design.fontSmallLabelBold2, anchor="w")
buttonContinue = tk.Button(framePaused, text="Continue", bg=LITHO_Design.colorBrightGreen, fg="white",
                           font=LITHO_Design.fontMiddleLabel2, activeforeground="white",
                           activebackground=LITHO_Design.colorBrightGreen, command=lambda: KeyInputCheck("continue"))
buttonStop = tk.Button(framePaused, text="Stop", bg=LITHO_Design.colorBrightRed, fg="white", font=LITHO_Design.fontMiddleLabel2,
                       activeforeground="white", activebackground=LITHO_Design.colorBrightRed,
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


frameSetting1 = tk.Frame(tabSetting, bg=LITHO_Design.colorDarkGray)
tabSetting.add(frameSetting1, text="Output Intensity")

frameSetting2 = tk.Frame(tabSetting, bg=LITHO_Design.colorDarkGray)
tabSetting.add(frameSetting2, text="System Info")

frameSetting3 = tk.Frame(tabSetting, bg=LITHO_Design.colorDarkGray)
tabSetting.add(frameSetting3, text="Lithography")

frameSetting4 = tk.Frame(tabSetting, bg=LITHO_Design.colorDarkGray)
tabSetting.add(frameSetting4, text="Go Back")



#=======================
# tabSetting-frameSetting1
#=======================
frameIntensityInSetting = tk.Frame(frameSetting1, height=100, width=355, bg=LITHO_Design.colorDarkGray,
                               highlightbackground="yellow", highlightthickness=2)


#=======================
# tabSetting-frameSetting1-frameIntensityInSetting
#=======================
labelIntensityInSetting1 = tk.Label(frameIntensityInSetting, text="Intensity (mW/cm²)", bg=LITHO_Design.colorDarkGray, fg="white",
                                font=LITHO_Design.fontSmallLabel)
labelIntensityInSetting2 = tk.Label(frameIntensityInSetting, text=outputIntensity, bg=LITHO_Design.colorDarkGray, fg="yellow",
                                font=LITHO_Design.fontMiddleLabel)

# Positioning

frameIntensityInSetting.place(x=230, y=40)
labelIntensityInSetting1.place(in_=frameIntensityInSetting, x=0, y=5, width=335, height=25)
labelIntensityInSetting2.place(in_=frameIntensityInSetting, x=0, y=40, width=335, height=55)


#==========================
# tabSetting-frameSetting2
#==========================

labelFirmwareVersion = tk.Label(frameSetting2, text="Software Version: CBLI-A-01-01", bg=LITHO_Design.colorDarkGray,
                                fg="white", font=LITHO_Design.fontSmallLabelBold2)
labelTotalTime = tk.Label(frameSetting2, text="Accumulated Exposure Time: [ 120hr,  32min, 07sec ]",
                          bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontSmallLabelBold2)

labelSerialNumber = tk.Label(frameSetting2, text= "Serial Number: 000000000124", bg=LITHO_Design.colorDarkGray,
                                fg="white", font=LITHO_Design.fontSmallLabelBold2)

labelTotalEnergy = tk.Label(frameSetting2, text= "Accumulated Exposure Energy: [12M J]", bg=LITHO_Design.colorDarkGray,
                                fg="white", font=LITHO_Design.fontSmallLabelBold2)

# Positioning
labelFirmwareVersion.place(in_=frameSetting2, x=30, y=100)
labelTotalTime.place(in_=frameSetting2, x=30, y=200)

labelSerialNumber.place(in_=frameSetting2, x=30, y= 50)
labelTotalEnergy.place(in_=frameSetting2, x= 30, y= 150)


#=======================
# tabSetting-frameSetting3 (Lithography)
#=======================

fig = Figure(figsize=(12, 5), facecolor='white')

axis  = fig.add_subplot(111)                  # 1 row, 1 column

xValues  = [1,2,3,4]

yValues0 = [6,7.5,8,7.5]
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
# Root-frameSplash
#================================
# variable
tempImage3 = PhotoImage(file="../images/cella_logo.png")
tempImage3 = tempImage3.subsample(2, 2) #이미지 작게 만들기
# UI component
Splash_Logo = tk.Label(frameSplash, image=tempImage3, bg="black")
labelForLogo = tk.Label(frameSplash, text="Please touch the screen", bg="black", fg="white", font=LITHO_Design.fontSmallLabel)

# Positioning
Splash_Logo.place(in_=frameSplash, x=0, y=0, width=800, height=480)
labelForLogo.place(in_=frameSplash, x=300, y=390, width=220, height=20)

# Binding
Splash_Logo.bind("<Button-1>", lambda event: OpStatusChange("FIRST_TOUCH"))



#===============================
# Root - frameWarning
#===============================

def actionButtonWarningGoback():
    frameWarning.grab_release()
    frameWarning.lower()
    KeyInputCheck("clear")

def actionButtonWarningOK():
    global exposureTime
    global exposureEnergy

    frameWarning.grab_release()
    frameWarning.lower()
    exposureTime = round(float(labelTime2.cget('text')), 1)
    exposureEnergy = round(exposureTime * outputIntensity, 1)
    OpStatusChange("READY")


labelWarningMsg = tk.Label(frameWarning, text="Current Setting is outranged by qualified level.\n"
                                              "\n""Do you want to set anyway?",
                           bg=LITHO_Design.colorDarkGray,fg="white", font=LITHO_Design.fontSmallMiddleLabel,
                           )
# borderwidth=2, relief="groove"
# labelWaningOK = tk.Label(frameWarning, text="OK")
# labelWarningGoback = tk.Label(frameWarning, text="Go back")
buttonWarningGoback = tk.Button(frameWarning, highlightthickness=0, text="Go back", bg=LITHO_Design.colorGreen, fg="white",
                            font=LITHO_Design.fontSmallMiddleLabel, activeforeground="white", activebackground=LITHO_Design.colorGreen,
                            command=lambda: actionButtonWarningGoback())
buttonWarningOK = tk.Button(frameWarning, highlightthickness=0, text="Set anyway", bg=LITHO_Design.colorGray, fg="white",
                            font=LITHO_Design.fontSmallMiddleLabel, activeforeground="white", activebackground=LITHO_Design.colorGray,
                            command=lambda: actionButtonWarningOK())

labelWarningMsg.grid(row=0,column=0,columnspan=2,sticky="new",ipadx=20,ipady=20,pady=5)
buttonWarningOK.grid(row=2,column=1,pady=1, ipadx=3)
buttonWarningGoback.grid(row=2,column=0, pady=1)
# buttonWarningOK.place(in_=frameWarning, x=0, y=0, width=800, height=480)
# labelWarningOK.place(in_=frameSplash, x=0, y=0, width=800, height=480)
# labelWarningGoback.place(in_=frameSplash, x=300, y=390, width=220, height=20)

#========================
# Style
#========================
style = ttk.Style()
style.theme_create("customTabStyle", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
    "TNotebook.Tab": {
        "configure": {"padding": [20, 10], "background": LITHO_Design.colorBrightGray, "foreground": "white",
                      "font": ('family Calibri', '12', 'bold')},
        "map": {"background": [("selected", LITHO_Design.colorDarkGray)],
                "expand": [("selected", [1, 1, 1, 0])]}}})

style.theme_use("customTabStyle")



frameSplash.lift()

#======================
# Start GUI
#=======================
root.mainloop()



if __name__ == '__main__':
    print(sys.path)