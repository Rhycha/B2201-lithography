from pj_litho_codes.codes.LITHO_package import LITHO_Design
import tkinter as tk
import enum
import threading
# import serial #? package 설치가 왜 안될까. 아하 아마
import sys
import random
from os import path

fDir    = path.dirname(__file__)
exposureTime = 12.0
elapsedTime = 0.0
exposureEnergy = 240.0
outputPower = 20.0
ledCurrent = 0
temperature = 42
firstEntered = True
sensorValue = 0



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
            threading.Timer(0.1, self.exposureTask).start()

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
                tempString = str(round(elapsedTime * outputPower, 1)) + '/' + str(exposureEnergy)
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

    if tabText == "Output Power" and opStatus == OpStatus.SETTING:
        frameButton.lift()
    elif tabText == "System Info" and opStatus == OpStatus.SETTING:
        tabSetting.lift()


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
            labelPausedEnergy.configure(text=str(round(elapsedTime * outputPower, 1)))
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
                        labelTime2.configure(text=tempString + '.')

                elif string == "clear":
                    tempNumber = 0
                    labelTime2.configure(text=str(tempNumber))
                    labelEnergy2.configure(text=str(tempNumber * outputPower))

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

                    tempNumber = float(round(tempNumber * outputPower, 1))
                    labelEnergy2.configure(text=str(tempNumber))


            elif opStatus == OpStatus.ENERGY_INPUT:
                if string == "point":
                    tempString = str(labelEnergy2.cget('text'))
                    if '.' not in tempString:
                        labelEnergy2.configure(text=tempString + '.')

                elif string == "clear":
                    tempNumber = 0
                    labelTime2.configure(text=str(tempNumber))
                    labelEnergy2.configure(text=str(tempNumber * outputPower))

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
                            if tempNumber > 600 * outputPower:
                                tempNumber = 600 * outputPower
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

                    tempNumber = float(round(tempNumber / outputPower, 1))
                    labelTime2.configure(text=str(tempNumber))


    elif opStatus == OpStatus.READY:
        if string == "startStop":
            OpStatusChange("EXPOSURE")
            # setDAC()

        if string == "setting":
            OpStatusChange("SETTING")

    elif opStatus == OpStatus.EXPOSURE:
        if string == "startStop":
            buttonStartStop.configure(state=tk.DISABLED)
            OpStatusChange("PAUSED")
            labelCurrent2.configure(text="0")


    elif opStatus == OpStatus.PAUSED:
        if string == "continue":
            frameTop.lift()
            buttonStartStop.configure(state=tk.NORMAL)
            OpStatusChange("EXPOSURE")


        if string == "stop":
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
            labelPower2.configure(text=str(outputPower))

        else:
            if string == "point":
                tempString = str(labelPowerInSetting2.cget('text'))
                if '.' not in tempString:
                    labelPowerInSetting2.configure(text=tempString + '.')

            elif string == "clear":
                tempNumber = 0
                labelPowerInSetting2.configure(text=str(tempNumber))
                labelEnergy2.configure(text=str(tempNumber * outputPower))

            else:
                if firstEntered == False:
                    if float(labelPowerInSetting2.cget('text')) != 0:
                        tempNumber = round(100 * float(labelPowerInSetting2.cget('text')))
                        tempNumber = tempNumber % 10
                        if tempNumber == 0:
                            tempString = str(labelPowerInSetting2.cget('text')) + string
                        else:
                            tempString = str(labelPowerInSetting2.cget('text'))

                        tempNumber = round(float(tempString), 1)
                        labelPowerInSetting2.configure(text=tempString)

                    else:
                        tempNumber = int(string)
                        labelPowerInSetting2.configure(text=string)

                elif firstEntered == True:
                    tempNumber = int(string)
                    labelPowerInSetting2.configure(text=string)
                    firstEntered = False

                tempNumber = float(round(tempNumber * exposureTime, 1))
                labelEnergy2.configure(text=str(tempNumber))