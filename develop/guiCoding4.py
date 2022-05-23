import common
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
import enum
import threading
import sys

# model.변수와 변수를 동시에 쓸 수 있다.
import model
from model import exposureTime, elapsedTime, exposureEnergy, outputPower, ledCurrent, temperature
from uart import setDAC, clearDAC, read_data, doSthDAC, update_model
from uart import UART
uart = UART()
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
        ##        print ('Exposure Task is running')    ## print generate large delay during timer run
        if(opStatus == OpStatus.EXPOSURE):
            threading.Timer(0.1, self.exposureTask).start()

            if round(model.elapsedTime, 1) < round(model.exposureTime, 1):
                if model.elapsedTime == 0:
                    # setDAC()
                    uart.setDAC()

                else:
                    #update_model brings three values from model: received_data, str current, sensorvalue
                    # _,str_current, str_sensor = update_model()
                    _,str_current, str_sensor = uart.update_model()

                    labelCurrent2.configure(text = str_current)
                    labelSensor2.configure(text = str_sensor)

                model.elapsedTime += 0.1
                tempString = str(round(model.elapsedTime, 1)) + '/' + str(model.exposureTime)
                labelTime2.configure(text = tempString)
                tempString = str(round(model.elapsedTime * model.outputPower, 1)) + '/' + str(model.exposureEnergy)
                labelEnergy2.configure(text = tempString)

                # doSthDAC()
                uart.doSthDAC()

            else:
                labelTime2.configure(text = str(model.exposureTime))
                labelEnergy2.configure(text = str(model.exposureEnergy))
                model.elapsedTime = 0

                #for checking
                # model.received_data = read_data()
                model.received_data = uart.read_data()

                print(model.received_data.hex())

                # clearDAC()
                uart.clearDAC()

                labelCurrent2.configure(text = "0")
                OpStatusChange("READY")

    # def get_ledCurrent(self):
    #     received_data = read_data()
    #     ledCurrent = received_data[0] * 256 + received_data[1]
    #     ledCurrent = ledCurrent * 3300 / 4095 / 110
    #     tempString = str(round(ledCurrent, 1))
    #     return received_data, tempString


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

    if string == "READY":
        frameTime.configure(highlightthickness = "0")
        frameEnergy.configure(highlightthickness = "0")
        labelTime2.configure(text = str(model.exposureTime))
        labelEnergy2.configure(text = str(model.exposureEnergy))
        labelTime2.configure(fg = "white")
        labelEnergy2.configure(fg = "white")

        if opStatus == OpStatus.EXPOSURE or opStatus == OpStatus.PAUSED:
            buttonStartStop.configure(bg = common.colorGreen, activebackground = common.colorGreen, text = "START")

        model.firstEntered = True
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

            buttonStartStop.configure(bg = common.colorRed, activebackground = common.colorRed, text = "STOP")
            opStatus = OpStatus.EXPOSURE
            at.exposureTask()

        if opStatus == OpStatus.PAUSED:

            opStatus = OpStatus.EXPOSURE
            at.exposureTask()
            
        print("OpStatus: EXPOSURE")

    elif string == "PAUSED":
        if opStatus == OpStatus.EXPOSURE:
            opStatus = OpStatus.PAUSED

            labelPausedTime.configure(text = str(round(model.elapsedTime, 1)))
            labelPausedEnergy.configure(text = str(round(model.elapsedTime * model.outputPower, 1)))
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
    if opStatus == OpStatus.TIME_INPUT or opStatus == OpStatus.ENERGY_INPUT:
    
        if string == "cancel":
            OpStatusChange("READY")
        elif string == "confirm":

            model.exposureTime = round(float(labelTime2.cget('text')), 1)
            model.exposureEnergy = round(model.exposureTime * model.outputPower, 1)
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
                    labelEnergy2.configure(text = str(tempNumber * model.outputPower))

                else:
                    if model.firstEntered == False:
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
                        
                    elif model.firstEntered == True:
                        tempNumber = int(string)
                        labelTime2.configure(text = string)
                        model.firstEntered = False

                    tempNumber = float(round(tempNumber * model.outputPower, 1))
                    labelEnergy2.configure(text = str(tempNumber))
                        

            elif opStatus == OpStatus.ENERGY_INPUT:
                if string == "point":
                    tempString = str(labelEnergy2.cget('text'))
                    if '.' not in tempString:
                        labelEnergy2.configure(text = tempString + '.')

                elif string == "clear":
                    tempNumber = 0
                    labelTime2.configure(text = str(tempNumber))
                    labelEnergy2.configure(text = str(tempNumber * model.outputPower))

                else:
                    if model.firstEntered == False:
                        if float(labelEnergy2.cget('text')) != 0:
                            tempNumber = round(100*float(labelEnergy2.cget('text')))
                            tempNumber = tempNumber % 10
                            if tempNumber == 0:
                                tempString = str(labelEnergy2.cget('text')) + string
                            else:
                                tempString = str(labelEnergy2.cget('text'))
                            
                            tempNumber = round(float(tempString), 1)
                            if tempNumber > 600* model.outputPower:
                                tempNumber = 600 * model.outputPower
                                labelEnergy2.configure(text =  str(tempNumber))
                            else:
                                labelEnergy2.configure(text =  tempString)
                        else:
                            tempNumber = int(string)
                            labelEnergy2.configure(text = string)

                    elif model.firstEntered == True:
                        tempNumber = int(string)
                        labelEnergy2.configure(text = string)
                        model.firstEntered = False
                    
                    tempNumber = float(round(tempNumber / model.outputPower, 1))
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
            # clearDAC()
            uart.clearDAC()

    elif opStatus == OpStatus.PAUSED:
        if string =="continue":
            frameTop.lift()
            buttonStartStop.configure(state=tk.NORMAL)
            OpStatusChange("EXPOSURE")
            # setDAC()
            uart.setDAC()

        if string =="stop":
            buttonStartStop.configure(state=tk.NORMAL)
            model.elapsedTime = 0.0
            OpStatusChange("READY")

    elif opStatus == OpStatus.SETTING:
        if string == "cancel":
            OpStatusChange("READY")
        elif string == "confirm":
            model.outputPower = round(float(labelPowerInSetting2.cget('text')), 1)
            model.exposureEnergy = round(model.exposureTime * model.outputPower, 1)
            OpStatusChange("READY")
            labelPower2.configure(text = str(model.outputPower))

        else:
            if string == "point":
                tempString = str(labelPowerInSetting2.cget('text'))
                if '.' not in tempString:
                    labelPowerInSetting2.configure(text = tempString + '.')

            elif string == "clear":
                tempNumber = 0 
                labelPowerInSetting2.configure(text = str(tempNumber))
                labelEnergy2.configure(text = str(tempNumber * model.outputPower))

            else:
                if model.firstEntered == False:
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
                    
                elif model.firstEntered == True:
                    tempNumber = int(string)
                    labelPowerInSetting2.configure(text = string)
                    model.firstEntered = False

                    
                tempNumber = float(round(tempNumber * model.exposureTime, 1))
                labelEnergy2.configure(text = str(tempNumber))
            


######## UI section ######## 
    
#### UI component initialization
global root                
root = tk.Tk()
root.wm_geometry("800x480")
root.resizable(False, False)
root.attributes('-fullscreen', True)

frameTop = tk.Frame(root, height = 480, width = 800, bg = common.colorDarkGray)
frameButton = tk.Frame(root, height = 290, width = 800, bg = common.colorDarkGray)
subframeButton1 = tk.Frame(frameButton, height = 210, width = 525, bg = common.colorDarkGray)
subframeButton2 = tk.Frame(frameButton, height = 210, width = 210, bg = common.colorDarkGray)

frameTop.place(x = 0, y = 0)
frameButton.place(x = 1, y = 190)   ## to hide 1 pixel vertical line by tabSetting notebook widget
subframeButton1.place(in_ = frameButton, x = 20, y = 25)
subframeButton2.place(in_ = frameButton, x = 570, y = 25)

frameTime  = tk.Frame(frameTop, height = 130, width = 355, bg = common.colorBrightGray, highlightbackground = "yellow")
labelTime1 = tk.Label(frameTime, text = "Exposure Time (sec)", bg = common.colorBrightGray, fg = "white", font = common.fontSmallLabel)
labelTime2 = tk.Label(frameTime, text =model.exposureTime, bg = common.colorBrightGray, fg ="white", font = common.fontMiddleLabel)

frameTime.bind("<Button-1>",  lambda event: OpStatusChange("TIME_INPUT"))
labelTime1.bind("<Button-1>",  lambda event: OpStatusChange("TIME_INPUT"))
labelTime2.bind("<Button-1>",  lambda event: OpStatusChange("TIME_INPUT"))

frameEnergy  = tk.Frame(frameTop, height = 130, width = 355, bg = common.colorBrightGray, highlightbackground = "yellow")
labelEnergy1 = tk.Label(frameTop, text = "Exposure Energy (mJ/cm²)", bg = common.colorBrightGray, fg = "white", font = common.fontSmallLabel)
labelEnergy2 = tk.Label(frameTop, text =model.exposureEnergy, bg = common.colorBrightGray, fg ="white", font = common.fontMiddleLabel)

frameEnergy.bind("<Button-1>",  lambda event: OpStatusChange("ENERGY_INPUT"))
labelEnergy1.bind("<Button-1>",  lambda event: OpStatusChange("ENERGY_INPUT"))
labelEnergy2.bind("<Button-1>",  lambda event: OpStatusChange("ENERGY_INPUT"))

framePower  = tk.Frame(frameTop, height = 100, width = 220, bg = common.colorDarkGray)
labelPower1 = tk.Label(framePower, text = "Power (mW/cm²)", bg = common.colorDarkGray, fg = "white", font = common.fontSmallLabel)
labelPower2 = tk.Label(framePower, text =model.outputPower, bg = common.colorDarkGray, fg ="white", font = common.fontMiddleLabel)

frameCurrent  = tk.Frame(frameTop, height = 100, width = 180, bg = common.colorDarkGray)
labelCurrent1 = tk.Label(frameCurrent, text = "Current (A)", bg = common.colorDarkGray, fg = "white", font = common.fontSmallLabel)
labelCurrent2 = tk.Label(frameCurrent, text =model.ledCurrent, bg = common.colorDarkGray, fg ="white", font = common.fontMiddleLabel)

frameTemper = tk.Frame(frameTop, height = 100, width = 180, bg = common.colorDarkGray)
labelTemper1 = tk.Label(frameTemper, text = "Temperature (℃)", bg = common.colorDarkGray, fg = "white", font = common.fontSmallLabel)
labelTemper2 = tk.Label(frameTemper, text =model.temperature, bg = common.colorDarkGray, fg ="white", font = common.fontMiddleLabel)


frameTime.place(x = 30, y = 30, height = 130, width = 355)
labelTime1.place(in_= frameTime, x = 10, y = 10, width = 335, height = 30)
labelTime2.place(in_= frameTime, x = 10, y = 45, width = 335, height = 70)

frameEnergy.place(x = 415, y = 30)
labelEnergy1.place(in_= frameEnergy, x = 10, y = 10, width = 335, height = 30)
labelEnergy2.place(in_= frameEnergy, x = 10, y = 45, width = 335, height = 70)

framePower.place(x = 30, y = 350)
labelPower1.place(in_= framePower, x = 0, y = 5, width = 220, height = 25)
labelPower2.place(in_= framePower, x = 0, y = 40, width = 220, height = 55)

frameCurrent.place(x = 270, y = 350)
labelCurrent1.place(in_= frameCurrent, x = 0, y = 5, width = 180, height = 25)
labelCurrent2.place(in_= frameCurrent, x = 0, y = 40, width = 180, height = 55)

frameTemper.place(x = 470, y = 350)
labelTemper1.place(in_= frameTemper, x = 0, y = 5, width = 180, height = 25)
labelTemper2.place(in_= frameTemper, x = 0, y = 40, width = 180, height = 55)


buttonStartStop = tk.Button(frameTop, highlightthickness = 0, text = "START", bg = common.colorGreen, fg = "white", font = common.fontLargeLabel, activeforeground = "white", activebackground = common.colorGreen, command = lambda:KeyInputCheck("startStop"))
tempImage = PhotoImage(file="/home/pi/Desktop/lithography/gearImage.png")
tempImage = tempImage.subsample(6, 6)
buttonSetting = tk.Button(frameTop, highlightthickness = 0, image = tempImage, command = lambda:KeyInputCheck("setting"))

buttonStartStop.place(x = 30, y = 190, width = 740, height = 130)
buttonSetting.place(x = 670, y = 350, width = 100, height = 100)

buttonNum1 = tk.Button(subframeButton1, highlightthickness = 0, text = "1", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("1"))
buttonNum2 = tk.Button(subframeButton1, highlightthickness = 0, text = "2", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("2"))
buttonNum3 = tk.Button(subframeButton1, highlightthickness = 0, text = "3", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("3"))
buttonNum4 = tk.Button(subframeButton1, highlightthickness = 0, text = "4", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("4"))
buttonNum5 = tk.Button(subframeButton1, highlightthickness = 0, text = "5", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("5"))
buttonNum6 = tk.Button(subframeButton1, highlightthickness = 0, text = "6", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("6"))
buttonNum7 = tk.Button(subframeButton1, highlightthickness = 0, text = "7", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("7"))
buttonNum8 = tk.Button(subframeButton1, highlightthickness = 0, text = "8", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("8"))
buttonNum9 = tk.Button(subframeButton1, highlightthickness = 0, text = "9", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("9"))
buttonNum0 = tk.Button(subframeButton1, highlightthickness = 0, text = "0", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("0"))
buttonPoint = tk.Button(subframeButton2, highlightthickness = 0, text = ".", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("point"))
buttonClear = tk.Button(subframeButton2, highlightthickness = 0, text = "C", bg = common.colorGray, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGray, command = lambda:KeyInputCheck("clear"))
buttonCancel = tk.Button(subframeButton2, highlightthickness = 0, text = "X", bg = common.colorRed, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorRed, command = lambda:KeyInputCheck("cancel"))
buttonConfirm = tk.Button(subframeButton2, highlightthickness = 0, text = "O", bg = common.colorGreen, fg = "white", font = common.fontMiddleLabel, width = 1, activeforeground = "white", activebackground = common.colorGreen, command = lambda:KeyInputCheck("confirm"))

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

buttonNum1.grid(row=0, column=0, sticky="nwes", padx = 10, pady = 10)
buttonNum2.grid(row=0, column=1, sticky="nwes", padx = 10, pady = 10)
buttonNum3.grid(row=0, column=2, sticky="nwes", padx = 10, pady = 10)
buttonNum4.grid(row=0, column=3, sticky="nwes", padx = 10, pady = 10)
buttonNum5.grid(row=0, column=4, sticky="nwes", padx = 10, pady = 10)
buttonNum6.grid(row=1, column=0, sticky="nwes", padx = 10, pady = 10)
buttonNum7.grid(row=1, column=1, sticky="nwes", padx = 10, pady = 10)
buttonNum8.grid(row=1, column=2, sticky="nwes", padx = 10, pady = 10)
buttonNum9.grid(row=1, column=3, sticky="nwes", padx = 10, pady = 10)
buttonNum0.grid(row=1, column=4, sticky="nwes", padx = 10, pady = 10)
buttonPoint.grid(row=0, column=0, sticky="nsew", padx = 10, pady = 10)
buttonClear.grid(row=0, column=1, sticky="nwes", padx = 10, pady = 10)
buttonCancel.grid(row=1, column=0, sticky="nwes", padx = 10, pady = 10)
buttonConfirm.grid(row=1, column=1, sticky="nwes", padx = 10, pady = 10)

framePaused = tk.Frame(root, height = 310, width = 634, bg = common.colorIvory, highlightthickness = 2, highlightbackground = "gray")
labelPausedTitle = tk.Label(framePaused, text = "Exposure Paused", bg = common.colorIvory, fg = "black", font = common.fontMiddleLabelBold2)
labelPausedTimeFixed = tk.Label(framePaused, text = "Exposed Time (sec)", bg = common.colorIvory, fg = "black", font = common.fontSmallLabel2, anchor = "w")
labelPausedTime = tk.Label(framePaused, text = str(model.elapsedTime), bg = common.colorIvory, fg ="black", font = common.fontSmallLabelBold2, anchor ="w")
labelPausedEnergyFixed = tk.Label(framePaused, text = "Exposed Energy (mJ/cm²)", bg = common.colorIvory, fg = "black", font = common.fontSmallLabel2, anchor = "w")
labelPausedEnergy = tk.Label(framePaused, text = str(model.elapsedTime * model.outputPower), bg = common.colorIvory, fg ="black", font = common.fontSmallLabelBold2, anchor ="w")
buttonContinue = tk.Button(framePaused, text = "Continue", bg = common.colorBrightGreen, fg = "white", font = common.fontMiddleLabel2, activeforeground = "white", activebackground = common.colorBrightGreen, command = lambda:KeyInputCheck("continue"))
buttonStop = tk.Button(framePaused, text = "Stop", bg = common.colorBrightRed, fg = "white", font = common.fontMiddleLabel2, activeforeground = "white", activebackground = common.colorBrightRed, command = lambda:KeyInputCheck("stop"))

framePaused.place(x = 83, y = 85)
labelPausedTitle.place(in_= framePaused, x = 141, y = 25, width = 350, height = 45)
labelPausedTimeFixed.place(in_= framePaused, x = 30, y = 91, width = 320, height = 40)
labelPausedTime.place(in_= framePaused, x = 370, y = 91, width = 160, height = 40)
labelPausedEnergyFixed.place(in_= framePaused, x = 30, y = 126, width = 320, height = 40)
labelPausedEnergy.place(in_= framePaused, x = 370, y = 126, width = 160, height = 40)
buttonContinue.place(in_= framePaused, x = 30, y = 195, width = 270, height = 90)
buttonStop.place(in_= framePaused, x = 330, y = 195, width = 270, height = 90)



style = ttk.Style()
style.theme_create( "customTabStyle", parent="alt", settings={
           "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
           "TNotebook.Tab": {
               "configure": {"padding": [20, 10], "background": common.colorBrightGray, "foreground" : "white", "font" : ('family Calibri', '12', 'bold') },
               "map":       {"background": [("selected", common.colorDarkGray)],
                             "expand": [("selected", [1, 1, 1, 0])] } } } )

style.theme_use("customTabStyle")

tabSetting = ttk.Notebook(root, width=800, height=480)
tabSetting.place(x = 0, y = 0)

tabSetting.bind("<<NotebookTabChanged>>", tabChanged)

frameSetting1 = tk.Frame(tabSetting, bg = common.colorDarkGray)
tabSetting.add(frameSetting1, text="Output Power")

framePowerInSetting  = tk.Frame(frameSetting1, height = 100, width = 355, bg = common.colorDarkGray, highlightbackground = "yellow", highlightthickness = 2)
labelPowerInSetting1 = tk.Label(framePowerInSetting, text = "Power (mW/cm²)", bg = common.colorDarkGray, fg = "white", font = common.fontSmallLabel)
labelPowerInSetting2 = tk.Label(framePowerInSetting, text =model.outputPower, bg = common.colorDarkGray, fg ="yellow", font = common.fontMiddleLabel)
framePowerInSetting.place(x = 230, y = 40)
labelPowerInSetting1.place(in_= framePowerInSetting, x = 0, y = 5, width = 335, height = 25)
labelPowerInSetting2.place(in_= framePowerInSetting, x = 0, y = 40, width = 335, height = 55)

frameSetting2 = tk.Frame(tabSetting, bg = common.colorDarkGray)
tabSetting.add(frameSetting2, text="System Info")
labelFirmwareVersion=tk.Label(frameSetting2, text="Software Version: CBLI-A-01-01", bg = common.colorDarkGray,  fg = "white", font = common.fontSmallLabelBold2)
labelFirmwareVersion.place(in_ = frameSetting2, x = 30, y = 100)

labelTotalTime=tk.Label(frameSetting2, text="Accumulated Exposure Time: [ 120hr,  32min, 07sec ]", bg = common.colorDarkGray,  fg = "white", font = common.fontSmallLabelBold2)
labelTotalTime.place(in_ = frameSetting2, x = 30, y = 150)

frameSplash = tk.Frame(root, height = 480, width = 800, bg = common.colorDarkGray)
frameSplash.place(x = 0, y = 0)
tempImage2 = PhotoImage(file = "/home/pi/Desktop/lithography/cella_logo.png")
tempImage2 = tempImage2.subsample(2, 2)
labelForLogo = tk.Label(frameSplash, image = tempImage2, bg = "black")
labelForLogo.place(in_ = frameSplash, x = 0, y = 0, width = 800, height = 480)
labelForLogo.bind("<Button-1>",  lambda event: OpStatusChange("FIRST_TOUCH"))
labelForLogo = tk.Label(frameSplash, text = "Please touch the screen", bg = "black", fg = "white", font = common.fontSmallLabel)
labelForLogo.place(in_ = frameSplash, x = 300, y =390, width = 220, height = 20)

labelSensor1 = tk.Label(frameTop, text = "Sensor Value: ", bg = common.colorDarkGray, fg = "white", font = common.fontSmallLabel)
labelSensor2 = tk.Label(frameTop, text = "0", bg = common.colorDarkGray, fg = "white", font = common.fontSmallLabel)
labelSensor1.place(in_ = frameTop, x = 30, y = 7, width = 120, height = 18)
labelSensor2.place(in_ = frameTop, x = 150, y = 7, width = 150, height = 18)

labelExit = tk.Label(frameTop, bg = common.colorDarkGray)
labelExit.place(in_ = frameTop, x = 700, y = 0, width = 100, height = 18)
labelExit.bind("<Button-1>",  lambda event: OpStatusChange("EXIT"))

#frameTop.lift()
frameSplash.lift()

root.mainloop()

######## references
##       btnFrame.place_forget()
