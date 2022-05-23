exposureTime = 12.0
elapsedTime = 0.0
exposureEnergy = 240.0
outputPower = 20.0
ledCurrent = 0
temperature = 42
firstEntered = True
sensorValue = 0
received_data = []

# we have this but current and sensorvalue are updated with DAC read
def get_ledCurrent():
    global ledCurrent
    tempCurrent = received_data[0] * 256 + received_data[1]
    tempCurrent = tempCurrent * 3300 / 4095 / 110
    ledCurrent = tempCurrent
    str_ledCurrent = str(round(tempCurrent, 1))
    return str_ledCurrent

def get_sensorvalue():
    global sensorValue
    sensorValue = received_data[2]*256 + received_data[3]
