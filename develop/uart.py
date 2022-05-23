from abc import ABCMeta, abstractmethod
import model


# import serial
#
#
# ser = serial.Serial(
#     port='/dev/ttyAMA1',
#     baudrate=115200,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
#     timeout=1)
#
# def setDAC():
#     if model.outputPower > 170:
#         tempValue = int(170*4095/500)
#     else:
#         tempValue = int(model.outputPower*4095/500)
#     ser.write(bytes(bytearray([0xA0])))
#     ser.write(bytes(bytearray([0x00])))
#     ser.write(bytes(bytearray([tempValue >> 8])))
#     ser.write(bytes(bytearray([tempValue & 0x00ff])))
#
#     ser.write(bytes(bytearray([0xA0])))
#     ser.write(bytes(bytearray([0x01])))
#     ser.write(bytes(bytearray([0x0f])))
#     ser.write(bytes(bytearray([0xff])))
#
#
# def clearDAC():
#     ser.write(bytes(bytearray([0xA0])))
#     ser.write(bytes(bytearray([0x00])))
#     ser.write(bytes(bytearray([0x00])))
#     ser.write(bytes(bytearray([0x00])))
#
#     ser.write(bytes(bytearray([0xA0])))
#     ser.write(bytes(bytearray([0x01])))
#     ser.write(bytes(bytearray([0x00])))
#     ser.write(bytes(bytearray([0x00])))
#
# def doSthDAC():
#
#     ser.write(bytes(bytearray([0xB0])))
#     ser.write(bytes(bytearray([0x00])))
#     ser.write(bytes(bytearray([0x00])))
#     ser.write(bytes(bytearray([0x00])))
#
#     ser.write(bytes(bytearray([0xC0])))
#     ser.write(bytes(bytearray([0x00])))
#     ser.write(bytes(bytearray([0x00])))
#     ser.write(bytes(bytearray([0x00])))
#
# def read_data():
#     '''
#     serial data read from ser.inWaiting
#     :return: bytearray
#     '''
#     data_left = ser.inWaiting()
#     model.received_data = ser.read(data_left)
#     return model.received_data
#
# def update_ledCurrent():
#     tempCurrent = model.received_data[0] * 256 + model.received_data[1]
#     tempCurrent = tempCurrent * 3300 / 4095 / 110
#     model.ledCurrent = tempCurrent
#     str_ledCurrent = str(round(tempCurrent, 1))
#     return str_ledCurrent
#
# def update_sensorvalue():
#     model.sensorValue = model.received_data[2]*256 + model.received_data[3]
#     return str(model.sensorValue)
#
# def update_model():
#     data = read_data()
#     str_current = update_ledCurrent()
#     str_sensor = update_sensorvalue()
#
#     return data, str_current, str_sensor


# def calculate_current_from_data(data):
#     '''
#     :param data: recevied_data from read_data
#     :return:
#     '''


class abstract_UART():
    def __init__(self):
        pass

    def setDAC(self):
        pass

    def clearDAC(self):
        pass

    def doSthDAC(self):
        pass

    def read_data(self):
        pass

    def update_ledCurrent(self):
        pass

    def update_sensorvalue(self):
        pass

    def update_model(self):
        pass


class UART(abstract_UART):

    def __init__(self):
        import serial
        self.ser = serial.Serial(
            port='/dev/ttyAMA1',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

    def setDAC(self):
        if model.outputPower > 170:
            tempValue = int(170 * 4095 / 500)
        else:
            tempValue = int(model.outputPower * 4095 / 500)
        self.ser.write(bytes(bytearray([0xA0])))
        self.ser.write(bytes(bytearray([0x00])))
        self.ser.write(bytes(bytearray([tempValue >> 8])))
        self.ser.write(bytes(bytearray([tempValue & 0x00ff])))

        self.ser.write(bytes(bytearray([0xA0])))
        self.ser.write(bytes(bytearray([0x01])))
        self.ser.write(bytes(bytearray([0x0f])))
        self.ser.write(bytes(bytearray([0xff])))

    def clearDAC(self):
        self.ser.write(bytes(bytearray([0xA0])))
        self.ser.write(bytes(bytearray([0x00])))
        self.ser.write(bytes(bytearray([0x00])))
        self.ser.write(bytes(bytearray([0x00])))

        self.ser.write(bytes(bytearray([0xA0])))
        self.ser.write(bytes(bytearray([0x01])))
        self.ser.write(bytes(bytearray([0x00])))
        self.ser.write(bytes(bytearray([0x00])))

    def doSthDAC(self):
        self.ser.write(bytes(bytearray([0xB0])))
        self.ser.write(bytes(bytearray([0x00])))
        self.ser.write(bytes(bytearray([0x00])))
        self.ser.write(bytes(bytearray([0x00])))

        self.ser.write(bytes(bytearray([0xC0])))
        self.ser.write(bytes(bytearray([0x00])))
        self.ser.write(bytes(bytearray([0x00])))
        self.ser.write(bytes(bytearray([0x00])))

    def read_data(self):
        '''
        serial data read from self.ser.inWaiting
        :return: bytearray
        '''
        data_left = self.ser.inWaiting()
        model.received_data = self.ser.read(data_left)
        return model.received_data

    def update_ledCurrent(self):
        tempCurrent = model.received_data[0] * 256 + model.received_data[1]
        tempCurrent = tempCurrent * 3300 / 4095 / 110
        model.ledCurrent = tempCurrent
        str_ledCurrent = str(round(tempCurrent, 1))
        return str_ledCurrent

    def update_sensorvalue(self):
        model.sensorValue = model.received_data[2]*256 + model.received_data[3]
        str_sensorValue = str(model.sensorValue)
        return str_sensorValue

    def update_model(self):
        data = self.read_data()
        str_current = self.update_ledCurrent()
        str_sensor = self.update_sensorvalue()

        return data, str_current, str_sensor

class UART_for_test(abstract_UART):

    def __init__(self):
        pass

    def setDAC(self):
        pass

    def clearDAC(self):
        pass

    def doSthDAC(self):
        pass

    def read_data(self):
        return []

    def update_ledCurrent(self):
        import random
        model.ledCurrent = random.uniform(0, 2)
        str_current = str(round(model.ledCurrent, 1))
        return str_current

    def update_sensorvalue(self):
        import random
        model.sensorValue = random.uniform(1,1000)
        str_sensor = str(round(model.sensorValue),1)
        return str_sensor

    def update_model(self):
        data = self.read_data()
        str_current = self.update_ledCurrent()
        str_sensor = self.update_sensorvalue()

        return data, str_current, str_sensor