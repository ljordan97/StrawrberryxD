import serial


def setStepMode(device, mode):
    data = [20, mode]
    sendCmd(device, data)

def sendCmd(device, cmd)
    cmd = [170, 1] + [device, cmd]
    ser.write(cmd)     # write a string

ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print(ser.name)         # check which port was really used

# cmd = [170, 1, 20, 3]
setStepMode(1,3)

ser.close()             # close port
