import serial

from develop.guiCoding4 import outputPower


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

def doSthDAC():

    ser.write(bytes(bytearray([0xB0])))
    ser.write(bytes(bytearray([0x00])))
    ser.write(bytes(bytearray([0x00])))
    ser.write(bytes(bytearray([0x00])))

    ser.write(bytes(bytearray([0xC0])))
    ser.write(bytes(bytearray([0x00])))
    ser.write(bytes(bytearray([0x00])))
    ser.write(bytes(bytearray([0x00])))

def read_data():
    '''
    :return: bytearray
    '''
    data_left = ser.inWaiting()
    received_data = ser.read(data_left)
    return received_data


class URAT():

    def __init__(self):
        import serial
        ser = serial.Serial(
        port='/dev/ttyAMA1',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

    def setDAC(self):
        if outputPower > 170:
            tempValue = int(170 * 4095 / 500)
        else:
            tempValue = int(outputPower * 4095 / 500)
        ser.write(bytes(bytearray([0xA0])))
        ser.write(bytes(bytearray([0x00])))
        ser.write(bytes(bytearray([tempValue >> 8])))
        ser.write(bytes(bytearray([tempValue & 0x00ff])))

        ser.write(bytes(bytearray([0xA0])))
        ser.write(bytes(bytearray([0x01])))
        ser.write(bytes(bytearray([0x0f])))
        ser.write(bytes(bytearray([0xff])))

    def clearDAC(self):
        ser.write(bytes(bytearray([0xA0])))
        ser.write(bytes(bytearray([0x00])))
        ser.write(bytes(bytearray([0x00])))
        ser.write(bytes(bytearray([0x00])))

        ser.write(bytes(bytearray([0xA0])))
        ser.write(bytes(bytearray([0x01])))
        ser.write(bytes(bytearray([0x00])))
        ser.write(bytes(bytearray([0x00])))

    def doSthDAC(self):
        ser.write(bytes(bytearray([0xB0])))
        ser.write(bytes(bytearray([0x00])))
        ser.write(bytes(bytearray([0x00])))
        ser.write(bytes(bytearray([0x00])))

        ser.write(bytes(bytearray([0xC0])))
        ser.write(bytes(bytearray([0x00])))
        ser.write(bytes(bytearray([0x00])))
        ser.write(bytes(bytearray([0x00])))

    def read_data(self):
        '''
        :return: bytearray
        '''
        data_left = ser.inWaiting()
        received_data = ser.read(data_left)
        return received_data