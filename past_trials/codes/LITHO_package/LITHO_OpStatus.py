import tkinter as tk
import enum
import threading
# import serial #? package 설치가 왜 안될까. 아하 아마
import sys
import random
from os import path
from time import sleep

import develop.model
from .LITHO_Design import *

fDir    = path.dirname(__file__)
exposureTime = 12.0 # Predetermined value
elapsedTime = 0.0 # Measured valued after start
exposureEnergy = 240.0
outputPower = 20.0
ledCurrent = 0
temperature = 42
# firstEntered = True
sensorValue = 0
# stop_logging_thread = False


class OpStatus(enum.Enum):
    READY = 0
    TIME_INPUT = 1
    ENERGY_INPUT = 2
    EXPOSURE = 3
    PAUSED = 4
    SETTING = 5

class Status():

    def __init__(self, GUI):
        self.curState = OpStatus.READY
        self.gui = GUI
        self.firstEntered = True
        self.atask = AsyncTask(self.gui, self)

    def OpStatusChange(self, string):
           # global opStatus
        # global firstEntered

        if string == "READY":
            self.gui.frameTime.configure(highlightthickness="0")
            self.gui.frameEnergy.configure(highlightthickness="0")
            self.gui.labelTime2.configure(text=str(exposureTime))
            self.gui.labelEnergy2.configure(text=str(exposureEnergy))
            self.gui.labelTime2.configure(fg="white")
            self.gui.labelEnergy2.configure(fg="white")

            if self.curState == OpStatus.EXPOSURE or self.curState == OpStatus.PAUSED:
                self.gui.buttonStartStop.configure(bg=colorGreen, activebackground=colorGreen, text="START")

            self.firstEntered = True
            self.curState = OpStatus.READY
            self.gui.frameTop.lift()
            print("OpStatus: READY")

        elif (string == "TIME_INPUT"):
            if self.curState == OpStatus.READY or self.curState == OpStatus.ENERGY_INPUT:

                # if self.curState == OpStatus.ENERGY_INPUT:
                    # temp_exposureEnergy = self.gui.exposureEnergy.get()
                    # self.gui.exposureEnergy.set(round(temp_exposureEnergy,1))
                    # tempNumber = round(float(self.gui.labelEnergy2.cget('text')), 1)
                    # self.gui.labelEnergy2.configure(text=str(tempNumber))

                self.curState = OpStatus.TIME_INPUT
                self.gui.frameTime.configure(highlightthickness="2")
                self.gui.frameEnergy.configure(highlightthickness="0")
                self.gui.labelTime2.configure(fg="yellow")
                self.gui.labelEnergy2.configure(fg="white")
                self.gui.frameButton.lift()
                print("OpStatus: TIME_INPUT")

        elif string == "ENERGY_INPUT":
            if self.curState == OpStatus.READY or self.curState == OpStatus.TIME_INPUT:

                # if self.curState == OpStatus.TIME_INPUT:
                    # tempNumber = round(float(labelTime2.cget('text')), 1)
                    # labelTime2.configure(text=str(tempNumber))
                    # temp_exposureTime = self.gui.exposureTime.get()
                    # self.gui.exposureTime.set(round(temp_exposureTime,1))
                self.gui.frameTime.configure(highlightthickness="0")
                self.gui.frameEnergy.configure(highlightthickness="2")
                self.gui.labelTime2.configure(fg="white")
                self.gui.labelEnergy2.configure(fg="yellow")
                self.curState = OpStatus.ENERGY_INPUT
                self.gui.frameButton.lift()
                print("OpStatus: ENERGY_INPUT")

        elif string == "EXPOSURE":
            if self.curState == OpStatus.READY:
                self.gui.buttonStartStop.configure(bg=colorRed, activebackground=colorRed, text="STOP")
                self.curState = OpStatus.EXPOSURE
                self.atask.exposureTask()

            if self.curState == OpStatus.PAUSED:
                self.curState = OpStatus.EXPOSURE
                self.atask.exposureTask()

            print("OpStatus: EXPOSURE")

        elif string == "PAUSED":
            if self.curState == OpStatus.EXPOSURE:

                self.curState = OpStatus.PAUSED

                self.gui.labelPausedTime.configure(text=str(round(elapsedTime, 1)))
                self.gui.labelPausedEnergy.configure(text=str(round(elapsedTime * outputPower, 1)))
                self.gui.framePaused.lift()
                print("OpStatus: PAUSED")

        elif string == "SETTING":
            if self.curState == OpStatus.READY:

                self.curState = OpStatus.SETTING
                self.gui.tabSetting.lift()
                self.gui.frameButton.lift()
                print("OpStatus: SETTING")

        elif string == "FIRST_TOUCH":
            self.gui.frameTop.lift()

        elif string == "EXIT":
            self.gui.root.destroy()
            sys.exit()


class AsyncTask:
    def __init__(self, GUI, Status):
        self.gui = GUI
        self.status = Status
        self.elapsedTime = develop.model.elapsedTime.get()
        self.exposureTime = develop.model.exposureTime.get()
        self.exposureEnergy = develop.model.exposureEnergy.get()
        self.ledCurrent = develop.model.ledCurrent.get()
        self.sensorValue = develop.model.sensorValue.get()

    # @classmethod
    def exposureTask(self):
        # global elapsedTime
        print ('Exposure Task is running')    ## print generate large delay during timer run
        if (self.status.curState == OpStatus.EXPOSURE):
            print("145", self.status.curState)
            exposure_thread = threading.Timer(0.1, self.exposureTask) #event handling을 0.1초 단위로
            exposure_thread.setDaemon(True) #강제종료 했을 때 Thread 종료되게
            exposure_thread.start()

            if round(self.elapsedTime, 1) < round(self.exposureTime, 1):
                if self.elapsedTime == 0:
                    pass
                else:

                    self.ledCurrent.set(round(random.uniform(0, 5)))
                    # ledCurrent = round(random.uniform(0, 5))
                    # tempString = str(round(ledCurrent, 1))
                    # self.gui.labelCurrent2.configure(text=tempString)
                    develop.model.ledCurrent.set(self.ledCurrent)

                    self.sensorValue.set(round(random.uniform(1, 9)))
                    # sensorValue = round(random.uniform(1, 9))
                    # tempString = str(sensorValue)
                    # labelSensor2.configure(text=tempString)
                    develop.model.sensorValue.set(self.sensorValue)

                self.elapsedTime += 0.1
                print(self.elapsedTime)
                timeText = str(round(develop.model.elapsedTime, 1)) + '/' + str(develop.model.exposureTime)
                self.gui.timeText.set(timeText)
                # labelTime2.configure(text=tempString)
                energyText = str(round(develop.model.elapsedTime * outputPower, 1)) + '/' + str(
                    develop.model.exposureEnergy)
                self.gui.energyText.set(energyText)
                # self.gui.energyText = str(round(self.gui.elapsedTime * outputPower, 1)) + '/' + str(self.gui.exposureEnergy)
                # self.gui.labelEnergy2.configure(text=tempString)




            else:
                # self.gui.labelTime2.configure(text=str(exposureTime))
                # self.gui.labelEnergy2.configure(text=str(exposureEnergy))
                develop.model.exposureTime.set(self.exposureTime)
                develop.model.exposureEnergy.set(self.exposureEnergy)
                self.elapsedTime = 0
                develop.model.elapsedTime.set(self.elapsedTime)
                self.gui.labelCurrent2.configure(text="0")
                self.status.OpStatusChange("READY")

# at = AsyncTask()
# opStatus = OpStatus.READY







