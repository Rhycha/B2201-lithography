import develop.model
from develop.model import exposureTime
from .LITHO_OpStatus import *
# from . import *
from .LITHO_GUI_Logging import *
class Callbacks():

    def __init__(self, GUI, Status):
        self.gui = GUI
        self.status = Status
        # self.firstEntered = self.status.firstEntered
        self.thread = Logging()
        # self.stop_logging_thread = False

# TODO: stop_logging_thread를 KeyInputCheck에서 확인할게 아니라 Status에서 확인하는게 나을듯.
# TODO: exposureTime, exposureEnergy를 StringVar()로 지정하여 바꾸는게 자료형이 안정적일듯.
    def KeyInputCheck(self, string):
        # global firstEntered
        # global exposureTime
        # global exposureEnergy
        # global outputPower
        # global elapsedTime
        # global stop_logging_thread
        self.exposureTime = develop.model.exposureTime.get()
        self.exposureEnergy = develop.model.exposureEnergy.get()
        self.outputPower = develop.model.outputPower.get()
        self.elapsedTime = develop.model.elapsedTime.get()

        if self.status.curState == OpStatus.TIME_INPUT or self.status.curState == OpStatus.ENERGY_INPUT:

            if string == "cancel":
                self.status.OpStatusChange("READY")
            elif string == "confirm":

                # exposureTime = round(float(temp_exposureTime), 1)
                # exposureEnergy = round(exposureTime * outputPower, 1)
                # temp_exposureTime = self.gui.exposureTime.get()
                # exposureTime.set(round(temp_exposureTime, 1))
                exposureTime.set(round(self.exposureTime, 1))
                # temp_exposureEnergy = temp_exposureTime * self.gui.outputPower.get()
                # exposureEnergy = round(temp_exposureEnergy,1)
                self.exposureEnergy = round(self.exposureTime*self.outputPower, 1)

                self.status.OpStatusChange("READY")
            else:
                if self.status.curState == OpStatus.TIME_INPUT:
                    if string == "point":
                        self.tempTimeStr = str(self.exposureTime)
                        if '.' not in self.tempTimeStr:
                            self.tempTimeStr = self.tempTimeStr + '.'
                            self.exposureTime = self.tempTimeStr
                            develop.model.exposureTime.set(self.exposureTime)

                    elif string == "clear":
                        self.exposureTime = 0
                        self.exposureEnergy = 0
                        develop.model.exposureTime.set(0)
                        develop.model.exposureEnergy.set(0)
                        # tempNumber = 0
                        # labelTime2.configure(text=str(tempNumber))
                        # labelEnergy2.configure(text=str(tempNumber * outputPower))

                    else:
                        if develop.model.firstEntered == False:
                            # temp_exposureTime = self.gui.exposureTime.get()
                            # if (temp_exposureTime != 0):
                            if (self.exposureTime != 0):
                                # tempNumber = round(100 * temp_exposureTime)
                                # tempNumber = tempNumber % 10
                                self.tempTimeNum = round(100*self.exposureTime)
                                self.tempTimeNum = self.tempTimeNum % 10
                                if self.tempTimeNum == 0:
                                    self.tempTimeStr = str(self.exposureTime) + string
                                else:
                                    self.tempTimestr = str(self.exposureTime)

                                self.tempTimeNum = round(float(self.tempTimestr), 1)
                                if self.tempTimeNum > 600:
                                    self.tempTimeNum = 600
                                    develop.model.exposureTime.set(self.tempTimeNum)
                                    # labelTime2.configure(text=str(tempNumber))
                                else:
                                    develop.model.exposureTime.set(float(self.tempTimeNum))
                            else:
                                self.tempTimeNum = int(string)
                                develop.model.exposureTime.set(self.tempTimeNum)
                                # labelTime2.configure(text=string)

                        elif develop.model.firstEntered == True:
                            self.tempTimeNum = int(string)
                            develop.model.exposureTime(self.tempTimeNum)
                            # labelTime2.configure(text=string)
                            develop.model.firstEntered = False

                        self.tempEnerNum = float(round(self.tempTimeNum * develop.model.outputPower, 1))
                        develop.model.exposureEnergy(self.tempEnerNum)
                        # labelEnergy2.configure(text=str(tempNumber))


                elif self.status.curState == OpStatus.ENERGY_INPUT:
                    if string == "point":
                        # tempString = str(self.gui.exposureEnergy.get())
                        # tempString = str(labelEnergy2.cget('text'))
                        self.tempEnerStr = str(self.exposureEnergy)
                        if '.' not in self.tempEnerStr:
                            self.tempEnerStr = self.tempEnerStr + '.'
                            self.exposureEnergy = float(self.tempEnerStr)
                            develop.model.exposureEnergy.set(self.exposureEnergy)
                            # labelEnergy2.configure(text=tempString + '.')

                    elif string == "clear":
                        self.exposureTime = 0
                        self.exposureEnergy = 0
                        develop.model.exposureTime.set(0)
                        develop.model.exposureEnergy.set(0)
                        # tempNumber = 0
                        # labelTime2.configure(text=str(tempNumber))
                        # labelEnergy2.configure(text=str(tempNumber * outputPower))

                    else:
                        if develop.model.firstEntered == False:
                            if self.exposureEnergy != 0:
                                self.tempEnerNum = round(100 * self.exposureEnergy)
                                self.tempEnerNum = self.tempEnerNum % 10
                                # tempNumber = tempNumber % 10
                                if self.tempEnerNum == 0:
                                    self.tempEnerStr = str(self.exposureEnergy) + string
                                    # tempString = str(labelEnergy2.cget('text')) + string
                                else:
                                    self.tempEnerStr = str(self.exposureEnergy)
                                    # tempString = str(labelEnergy2.cget('text'))

                                # tempNumber = round(float(tempString), 1)
                                self.tempEnerNum = round(self.tempEnerStr, 1)
                                if self.tempEnerNum > 600 * self.outputPower:
                                    self.tempEnerNum = 600 * self.outputPower
                                    # labelEnergy2.configure(text=str(tempNumber))
                                    develop.model.exposureEnergy.set(self.tempEnerNum)

                                else:
                                    # labelEnergy2.configure(text=tempString)
                                    develop.model.exposureEnergy.set(float(self.tempEnerStr))
                            else:
                                # tempNumber = int(string)
                                self.tempEnerNum = int(string)
                                # labelEnergy2.configure(text=string)
                                develop.model.exposureEnergy(self.tempEnerNum)

                        elif develop.model.firstEntered == True:
                            self.tempEnerNum = int(string)
                            develop.model.exposureEnergy.set(self.tempEnerNum)
                            # labelEnergy2.configure(text=string)
                            develop.model.firstEntered = False

                        # tempNumber = float(round(tempNumber / outputPower, 1))
                        self.exposureTime.set(float(round(self.tempEnerNum / self.outputPower, 1)))

                        # labelTime2.configure(text=str(tempNumber))


        elif self.status.curState == OpStatus.READY:
            if string == "startStop":
                self.status.OpStatusChange("EXPOSURE")
                # stop_logging_thread = False #flag 변경 후 (init이 있으면 필요 없음.)

                self.thread.create_log_thread()
            if string == "setting":
                self.status.OpStatusChange("SETTING")

        elif self.status.curState == OpStatus.EXPOSURE:
            if string == "startStop":
                self.thread._stop() #log 기록 정지
                self.gui.buttonStartStop.configure(state=tk.DISABLED)
                self.status.OpStatusChange("PAUSED")
                develop.model.ledCurrent.set(0)
                # self.gui.labelCurrent2.configure(text="0")


        elif self.status.curState == OpStatus.PAUSED:
            if string == "continue":
                self.gui.frameTop.lift()
                self.gui.buttonStartStop.configure(state=tk.NORMAL)
                self.status.OpStatusChange("EXPOSURE")
                self.thread._ready() #flag를 다시 변경하고
                self.thread.create_log_thread() #log 기록 재시작


            if string == "stop":
                self.gui.buttonStartStop.configure(state=tk.NORMAL)
                self.elapsedTime = 0.0
                develop.model.elapsedTime.set(0.0)
                self.status.OpStatusChange("READY")

        elif self.status.curState == OpStatus.SETTING:
            if string == "cancel":
                self.status.OpStatusChange("READY")
            elif string == "confirm":
                self.outputPower = round(self.outputPower, 1)
                self.exposureEnergy = round(self.exposureTime * self.outputPower, 1)
                self.status.OpStatusChange("READY")
                develop.model.outputPower.get(self.outputPower)

            else:
                if string == "point":
                    # tempString = str(self.gui.labelPowerInSetting2.cget('text'))
                    self.tempPowerStr = str(self.outputPower)
                    if '.' not in self.tempPowerStr:
                        self.tempPowerStr = self.tempPowerStr + '.'
                        develop.model.outputPower.set((float(self.tempPowerStr)))
                        # self.gui.labelPowerInSetting2.configure(text=tempString + '.')

                elif string == "clear":
                    self.outputPower = 0
                    self.tempPowerNum = self.outputPower
                    develop.model.outputPower.set(self.outputPower)
                    # self.gui.labelPowerInSetting2.configure(text=str(tempNumber))
                    self.exposureEnergy = 0
                    self.tempPowerNum = self.exposureEnergy
                    develop.model.exposureEnergy.set(self.exposureEnergy)
                    # self.gui.labelEnergy2.configure(text=str(tempNumber * outputPower))

                else:
                    if self.statusfirstEntered == False:
                        if self.outputPower != 0:
                        # if float(self.gui.labelPowerInSetting2.cget('text')) != 0:
                        #     self.tempPowerNum = round(100 * float(self.gui.labelPowerInSetting2.cget('text')))
                        #     self.tempPowerNum = self.tempPowerNum % 10
                            self.tempPowerNum = round(100*self.outputPower)
                            self.tempPowerNum = self.tempPowerNum % 10
                            if self.tempPowerNum == 0:
                                self.tempPowerStr = str(self.outputPower) + string
                            else:
                                self.tempPowerStr = str(self.outputPower)

                            self.tempPowerNum = round(float(self.tempPowerStr), 1)
                            self.outputPower = self.tempPowerNum
                            develop.model.outputPower.set(self.outputPower)
                            # self.gui.labelPowerInSetting2.configure(text=self.tempPowerStr)

                        else:
                            self.tempPowerNum = int(string)
                            self.outputPower = self.tempPowerNum
                            develop.model.outputPower.set(self.outputPower)
                            # self.gui.labelPowerInSetting2.configure(text=string)

                    elif develop.model.firstEntered == True:
                        self.tempPowerNum = int(string)
                        self.outputPower = self.tempPowerNum
                        develop.model.outputPower.set(self.outputPower)
                        # self.gui.labelPowerInSetting2.configure(text=string)
                        develop.model.firstEntered = False

                    self.tempPowerNum = round(self.tempPowerNum * self.exposureTime, 1)
                    self.outputPower = self.tempPowerNum
                    develop.model.outputPower.set(self.outputPower)
                    # self.gui.labelEnergy2.configure(text=str(self.tempPowerNum))


    def tabChanged(self, event):
        selectedTab = event.widget.select()
        tabText = event.widget.tab(selectedTab, "text")

        if tabText == "Output Power" and self.status.curState == OpStatus.SETTING:
            self.gui.frameButton.lift() #Power input 넣기 위한 Keyboard 생성
        elif tabText == "System Info" and self.status.curState == OpStatus.SETTING:
            self.gui.tabSetting.lift()
        elif tabText == "Lithography" and self.status.curState == OpStatus.SETTING:
            self.gui.frameButton.lower()
        elif tabText == "Go Back" and self.status.curState == OpStatus.SETTING:
            self.KeyInputCheck("cancel")