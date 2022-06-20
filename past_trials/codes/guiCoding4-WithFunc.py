from pj_litho_codes.codes.LITHO_package import LITHO_Design
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
import enum
import threading
import serial
import sys

exposureTime = 12.0
elapsedTime = 0.0
exposureEnergy = 240.0
outputPower = 20.0
ledCurrent = 0
temperature = 42
firstEntered = True
sensorValue = 0

ser = serial.Serial(
    port='/dev/ttyAMA1',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)

def setDAC():
    if outputPower > 170:
        tempValue = int(170*4095/500)
    else:
        tempValue = int(outputPower*4095/500)
    ser.write(bytes(bytearray([0xA0])))
    ser.write(bytes(bytearray([0x00])))
    ser.write(bytes(bytearray([tempValue >> 8])))
    ser.write(bytes(bytearray([tempValue & 0x00ff])))

    ser.write(bytes(bytearray([0xA0])))
    ser.write(bytes(bytearray([0x01])))
    ser.write(bytes(bytearray([0x0f])))
    ser.write(bytes(bytearray([0xff])))

def clearDAC():
    ser.write(bytes(bytearray([0xA0])))
    ser.write(bytes(bytearray([0x00])))
    ser.write(bytes(bytearray([0x00])))
    ser.write(bytes(bytearray([0x00])))

    ser.write(bytes(bytearray([0xA0])))
    ser.write(bytes(bytearray([0x01])))
    ser.write(bytes(bytearray([0x00])))
    ser.write(bytes(bytearray([0x00])))

class OpStatus(enum.Enum):
    READY = 0
    TIME_INPUT = 1
    ENERGY_INPUT = 2
    EXPOSURE = 3
    PAUSED = 4
    SETTING  = 5

class AsyncTask:
    def __init__(self):
        pass

    def exposureTask(self):
        global elapsedTime
##        print ('Exposure Task is running')    ## print generate large delay during timer run 
        if(opStatus == OpStatus.EXPOSURE):
            threading.Timer(0.1, self.exposureTask).start()
            
            if round(elapsedTime, 1) < round(exposureTime, 1):
                if elapsedTime == 0:
                    setDAC()
                else:
                    data_left = ser.inWaiting()
                    received_data = ser.read(data_left)
                    ledCurrent = received_data[0]*256 + received_data[1]
                    ledCurrent = ledCurrent*3300/4095/110
                    tempString = str(round(ledCurrent, 1))
                    #tempString = str(ledCurrent)
                    labelCurrent2.configure(text = tempString)

                    sensorValue = received_data[2]*256 + received_data[3]
                    tempString = str(sensorValue)
                    labelSensor2.configure(text = tempString)

                elapsedTime += 0.1
                tempString = str(round(elapsedTime, 1)) + '/' + str(exposureTime)
                labelTime2.configure(text = tempString)
                tempString = str(round(elapsedTime*outputPower, 1)) + '/' + str(exposureEnergy)
                labelEnergy2.configure(text = tempString)

                ser.write(bytes(bytearray([0xB0])))
                ser.write(bytes(bytearray([0x00])))
                ser.write(bytes(bytearray([0x00])))
                ser.write(bytes(bytearray([0x00])))

                ser.write(bytes(bytearray([0xC0])))
                ser.write(bytes(bytearray([0x00])))
                ser.write(bytes(bytearray([0x00])))
                ser.write(bytes(bytearray([0x00])))

                
            else:
                labelTime2.configure(text = str(exposureTime))
                labelEnergy2.configure(text = str(exposureEnergy))
                elapsedTime = 0
                
                data_left = ser.inWaiting()
                received_data = ser.read(data_left)
                print(received_data.hex())
                
                clearDAC()
                labelCurrent2.configure(text = "0")
                OpStatusChange("READY")


at = AsyncTask()
opStatus = OpStatus.READY


def testFunction(event):
    print("testFuction Called")
    

def tabChanged(event):
        selectedTab = event.widget.select()
        tabText = event.widget.tab(selectedTab, "text")

        if tabText == "Output Power" and opStatus == OpStatus.SETTING:
            frameButton.lift()
        elif tabText == "System Info" and opStatus == OpStatus.SETTING:
            tabSetting.lift()


def OpStatusChange(string):
    global opStatus
    global firstEntered
    
    if string == "READY":
        frameTime.configure(highlightthickness = "0")
        frameEnergy.configure(highlightthickness = "0")
        labelTime2.configure(text = str(exposureTime))
        labelEnergy2.configure(text = str(exposureEnergy))
        labelTime2.configure(fg = "white")
        labelEnergy2.configure(fg = "white")

        if opStatus == OpStatus.EXPOSURE or opStatus == OpStatus.PAUSED:
            buttonStartStop.configure(bg = LITHO_Design.colorGreen, activebackground = LITHO_Design.colorGreen, text ="START")

        firstEntered = True
        opStatus = OpStatus.READY
        frameTop.lift()
        print("OpStatus: READY")

    elif (string == "TIME_INPUT") :
        if opStatus == OpStatus.READY or opStatus == OpStatus.ENERGY_INPUT:

            if opStatus == OpStatus.ENERGY_INPUT:
               tempNumber = round(float(labelEnergy2.cget('text')), 1)
               labelEnergy2.configure(text = str(tempNumber))

            opStatus = OpStatus.TIME_INPUT
            frameTime.configure(highlightthickness = "2")
            frameEnergy.configure(highlightthickness = "0")
            labelTime2.configure(fg = "yellow")
            labelEnergy2.configure(fg = "white")
            frameButton.lift()
            print("OpStatus: TIME_INPUT")

    elif string == "ENERGY_INPUT":
        if opStatus == OpStatus.READY or opStatus == OpStatus.TIME_INPUT:

            if opStatus == OpStatus.TIME_INPUT:
                tempNumber = round(float(labelTime2.cget('text')), 1)
                labelTime2.configure(text = str(tempNumber))
            
            frameTime.configure(highlightthickness = "0")
            frameEnergy.configure(highlightthickness = "2")
            labelTime2.configure(fg = "white")
            labelEnergy2.configure(fg = "yellow")
            opStatus = OpStatus.ENERGY_INPUT
            frameButton.lift()
            print("OpStatus: ENERGY_INPUT")

    elif string == "EXPOSURE":
        if opStatus == OpStatus.READY:

            buttonStartStop.configure(bg = LITHO_Design.colorRed, activebackground = LITHO_Design.colorRed, text ="STOP")
            opStatus = OpStatus.EXPOSURE
            at.exposureTask()

        if opStatus == OpStatus.PAUSED:

            opStatus = OpStatus.EXPOSURE
            at.exposureTask()
            
        print("OpStatus: EXPOSURE")

    elif string == "PAUSED":
        if opStatus == OpStatus.EXPOSURE:
            opStatus = OpStatus.PAUSED

            labelPausedTime.configure(text = str(round(elapsedTime, 1)))
            labelPausedEnergy.configure(text = str(round(elapsedTime * outputPower, 1)))
            framePaused.lift()
            print("OpStatus: PAUSED")
            
    elif string == "SETTING":
        if opStatus == OpStatus.READY:
            opStatus = OpStatus.SETTING
            tabSetting.lift()
            frameButton.lift()
            print("OpStatus: SETTING")

    elif string == "FIRST_TOUCH":
        frameTop.lift()

    elif string == "EXIT":
       root.destroy()
       sys.exit()


def KeyInputCheck(string):
    global firstEntered
    global exposureTime
    global exposureEnergy
    global outputPower
    global elapsedTime

    if opStatus == OpStatus.TIME_INPUT or opStatus == OpStatus.ENERGY_INPUT:
    
        if string == "cancel":
            OpStatusChange("READY")
        elif string == "confirm":

            exposureTime = round(float(labelTime2.cget('text')), 1)
            exposureEnergy = round(exposureTime * outputPower, 1)
            OpStatusChange("READY")
        else:
            if opStatus == OpStatus.TIME_INPUT:
                if string == "point":
                    tempString = str(labelTime2.cget('text'))
                    if '.' not in tempString:
                        labelTime2.configure(text = tempString + '.')

                elif string == "clear":
                    tempNumber = 0 
                    labelTime2.configure(text = str(tempNumber))
                    labelEnergy2.configure(text = str(tempNumber * outputPower))

                else:
                    if firstEntered == False:
                        if float(labelTime2.cget('text')) != 0:
                            tempNumber = round(100*float(labelTime2.cget('text')))
                            tempNumber = tempNumber % 10
                            if tempNumber == 0:
                                tempString = str(labelTime2.cget('text')) + string
                            else:
                                tempString = str(labelTime2.cget('text'))
                            
                            tempNumber = round(float(tempString), 1)
                            if tempNumber > 600:
                                tempNumber = 600
                                labelTime2.configure(text =  str(tempNumber))
                            else:
                                labelTime2.configure(text =  tempString)
                        else:
                            tempNumber = int(string)
                            labelTime2.configure(text = string)
                        
                    elif firstEntered == True:
                        tempNumber = int(string)
                        labelTime2.configure(text = string)
                        firstEntered = False

                    tempNumber = float(round(tempNumber * outputPower, 1))
                    labelEnergy2.configure(text = str(tempNumber))
                        

            elif opStatus == OpStatus.ENERGY_INPUT:
                if string == "point":
                    tempString = str(labelEnergy2.cget('text'))
                    if '.' not in tempString:
                        labelEnergy2.configure(text = tempString + '.')

                elif string == "clear":
                    tempNumber = 0
                    labelTime2.configure(text = str(tempNumber))
                    labelEnergy2.configure(text = str(tempNumber * outputPower))

                else:
                    if firstEntered == False:
                        if float(labelEnergy2.cget('text')) != 0:
                            tempNumber = round(100*float(labelEnergy2.cget('text')))
                            tempNumber = tempNumber % 10
                            if tempNumber == 0:
                                tempString = str(labelEnergy2.cget('text')) + string
                            else:
                                tempString = str(labelEnergy2.cget('text'))
                            
                            tempNumber = round(float(tempString), 1)
                            if tempNumber > 600*outputPower:
                                tempNumber = 600*outputPower
                                labelEnergy2.configure(text =  str(tempNumber))
                            else:
                                labelEnergy2.configure(text =  tempString)
                        else:
                            tempNumber = int(string)
                            labelEnergy2.configure(text = string)

                    elif firstEntered == True:
                        tempNumber = int(string)
                        labelEnergy2.configure(text = string)
                        firstEntered = False
                    
                    tempNumber = float(round(tempNumber / outputPower, 1))
                    labelTime2.configure(text = str(tempNumber))
                    

    elif opStatus == OpStatus.READY:
        if string =="startStop":
            OpStatusChange("EXPOSURE")
            #setDAC()

        if string == "setting":
            OpStatusChange("SETTING")

    elif opStatus == OpStatus.EXPOSURE:
        if string =="startStop":
            buttonStartStop.configure(state=tk.DISABLED)
            OpStatusChange("PAUSED")
            labelCurrent2.configure(text = "0")
            clearDAC()

    elif opStatus == OpStatus.PAUSED:
        if string =="continue":
            frameTop.lift()
            buttonStartStop.configure(state=tk.NORMAL)
            OpStatusChange("EXPOSURE")
            setDAC()

        if string =="stop":
            buttonStartStop.configure(state=tk.NORMAL)
            elapsedTime = 0.0
            OpStatusChange("READY")

    elif opStatus == OpStatus.SETTING:
        if string == "cancel":
            OpStatusChange("READY")
        elif string == "confirm":
            outputPower = round(float(labelPowerInSetting2.cget('text')), 1)
            exposureEnergy = round(exposureTime * outputPower, 1)
            OpStatusChange("READY")
            labelPower2.configure(text = str(outputPower))

        else:
            if string == "point":
                tempString = str(labelPowerInSetting2.cget('text'))
                if '.' not in tempString:
                    labelPowerInSetting2.configure(text = tempString + '.')

            elif string == "clear":
                tempNumber = 0 
                labelPowerInSetting2.configure(text = str(tempNumber))
                labelEnergy2.configure(text = str(tempNumber * outputPower))

            else:
                if firstEntered == False:
                    if float(labelPowerInSetting2.cget('text')) != 0:
                        tempNumber = round(100*float(labelPowerInSetting2.cget('text')))
                        tempNumber = tempNumber % 10
                        if tempNumber == 0:
                            tempString = str(labelPowerInSetting2.cget('text')) + string
                        else:
                            tempString = str(labelPowerInSetting2.cget('text'))
                 
                        tempNumber = round(float(tempString), 1)
                        labelPowerInSetting2.configure(text =  tempString)
                        
                    else:
                        tempNumber = int(string)
                        labelPowerInSetting2.configure(text = string)
                    
                elif firstEntered == True:
                    tempNumber = int(string)
                    labelPowerInSetting2.configure(text = string)
                    firstEntered = False

                    
                tempNumber = float(round(tempNumber * exposureTime, 1))
                labelEnergy2.configure(text = str(tempNumber))



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
frameTop = tk.Frame(root, height=480, width=800, bg=LITHO_Design.colorDarkGray)
frameButton = tk.Frame(root, height=290, width=800, bg=LITHO_Design.colorDarkGray)
framePaused = tk.Frame(root, height=310, width=634, bg=LITHO_Design.colorIvory, highlightthickness=2,
                       highlightbackground="gray")
tabSetting = ttk.Notebook(root, width=800, height=480)
frameSplash = tk.Frame(root, height=480, width=800, bg=LITHO_Design.colorDarkGray)


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
frameTime = tk.Frame(frameTop, height=130, width=355, bg=LITHO_Design.colorBrightGray, highlightbackground="yellow")
frameEnergy = tk.Frame(frameTop, height=130, width=355, bg=LITHO_Design.colorBrightGray, highlightbackground="yellow")
labelEnergy1 = tk.Label(frameTop, text="Exposure Energy (mJ/cm²)", bg=LITHO_Design.colorBrightGray, fg="white",
                        font=LITHO_Design.fontSmallLabel)
labelEnergy2 = tk.Label(frameTop, text=exposureEnergy, bg=LITHO_Design.colorBrightGray, fg="white",
                        font=LITHO_Design.fontMiddleLabel)
framePower = tk.Frame(frameTop, height=100, width=220, bg=LITHO_Design.colorDarkGray)
frameCurrent = tk.Frame(frameTop, height=100, width=180, bg=LITHO_Design.colorDarkGray)
frameTemper = tk.Frame(frameTop, height=100, width=180, bg=LITHO_Design.colorDarkGray)
buttonStartStop = tk.Button(frameTop, highlightthickness=0, text="START", bg=LITHO_Design.colorGreen, fg="white",
                            font=LITHO_Design.fontLargeLabel, activeforeground="white", activebackground=LITHO_Design.colorGreen,
                            command=lambda: KeyInputCheck("startStop"))
buttonSetting = tk.Button(frameTop, highlightthickness=0, image=tempImage, command=lambda: KeyInputCheck("setting"))
labelSensor1 = tk.Label(frameTop, text="Sensor Value: ", bg=LITHO_Design.colorDarkGray, fg="white",
                        font=LITHO_Design.fontSmallLabel)
labelSensor2 = tk.Label(frameTop, text="0", bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontSmallLabel)
labelExit = tk.Label(frameTop, bg=LITHO_Design.colorDarkGray)


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

# Binding
labelTime1.bind("<Button-1>", lambda event: OpStatusChange("TIME_INPUT"))
labelTime2.bind("<Button-1>", lambda event: OpStatusChange("TIME_INPUT"))

#================================
# frameTop-framePower
#================================
labelPower1 = tk.Label(framePower, text="Power (mW/cm²)", bg=LITHO_Design.colorDarkGray, fg="white",
                       font=LITHO_Design.fontSmallLabel)
labelPower2 = tk.Label(framePower, text=outputPower, bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontMiddleLabel)

#================================
# frameTop-frameCurrent
#================================
labelCurrent1 = tk.Label(frameCurrent, text="Current (A)", bg=LITHO_Design.colorDarkGray, fg="white",
                         font=LITHO_Design.fontSmallLabel)
labelCurrent2 = tk.Label(frameCurrent, text=ledCurrent, bg=LITHO_Design.colorDarkGray, fg="white",
                         font=LITHO_Design.fontMiddleLabel)

#================================
# frameTop-frameTemper
#================================
labelTemper1 = tk.Label(frameTemper, text="Temperature (℃)", bg=LITHO_Design.colorDarkGray, fg="white",
                        font=LITHO_Design.fontSmallLabel)
labelTemper2 = tk.Label(frameTemper, text=temperature, bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontMiddleLabel)


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
labelPausedEnergy = tk.Label(framePaused, text=str(elapsedTime * outputPower), bg=LITHO_Design.colorIvory, fg="black",
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
tabSetting.add(frameSetting1, text="Output Power")

frameSetting2 = tk.Frame(tabSetting, bg=LITHO_Design.colorDarkGray)
tabSetting.add(frameSetting2, text="System Info")


#=======================
# tabSetting-frameSetting1
#=======================
framePowerInSetting = tk.Frame(frameSetting1, height=100, width=355, bg=LITHO_Design.colorDarkGray,
                               highlightbackground="yellow", highlightthickness=2)


#=======================
# tabSetting-frameSetting1-framePowerInSetting
#=======================
labelPowerInSetting1 = tk.Label(framePowerInSetting, text="Power (mW/cm²)", bg=LITHO_Design.colorDarkGray, fg="white",
                                font=LITHO_Design.fontSmallLabel)
labelPowerInSetting2 = tk.Label(framePowerInSetting, text=outputPower, bg=LITHO_Design.colorDarkGray, fg="yellow",
                                font=LITHO_Design.fontMiddleLabel)

# Positioning

framePowerInSetting.place(x=230, y=40)
labelPowerInSetting1.place(in_=framePowerInSetting, x=0, y=5, width=335, height=25)
labelPowerInSetting2.place(in_=framePowerInSetting, x=0, y=40, width=335, height=55)


#==========================
# tabSetting-frameSetting2
#==========================
labelFirmwareVersion = tk.Label(frameSetting2, text="Software Version: CBLI-A-01-01", bg=LITHO_Design.colorDarkGray,
                                fg="white", font=LITHO_Design.fontSmallLabelBold2)
labelTotalTime = tk.Label(frameSetting2, text="Accumulated Exposure Time: [ 120hr,  32min, 07sec ]",
                          bg=LITHO_Design.colorDarkGray, fg="white", font=LITHO_Design.fontSmallLabelBold2)

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
labelForLogo = tk.Label(frameSplash, text="Please touch the screen", bg="black", fg="white", font=LITHO_Design.fontSmallLabel)

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
        "configure": {"padding": [20, 10], "background": LITHO_Design.colorBrightGray, "foreground": "white",
                      "font": ('family Calibri', '12', 'bold')},
        "map": {"background": [("selected", LITHO_Design.colorDarkGray)],
                "expand": [("selected", [1, 1, 1, 0])]}}})

style.theme_use("customTabStyle")



#======================
# Start GUI
#=======================
# frameTop.lift()
frameSplash.lift()

root.mainloop()

######## references
##       btnFrame.place_forget()
