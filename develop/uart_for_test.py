



if __name__ == "__main__":
    import model

    for i in range(0, 180, 10):
        model.outputPower = i
        if model.outputPower > 170:
            tempValue = int(170 * 4095 / 500)
        else:
            tempValue = int(model.outputPower * 4095 / 500)
        a = bytes(bytearray([0xA0]))
        b = bytes(bytearray([0x00]))
        c = bytes(bytearray([tempValue >> 8]))
        d = bytes(bytearray([tempValue & 0x00ff]))
        print(c)
        print(d)


