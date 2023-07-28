import serial
import time
SerialObj = serial.Serial('/dev/ttyUSB0', 115200, timeout=30, parity=serial.PARITY_EVEN, rtscts=1)# COMxx   format on Windows
SerialObj.baudrate = 115200  # set Baud rate to 9600
SerialObj.bytesize = 8     # Number of data bits = 8
SerialObj.parity   ='N'    # No parity
SerialObj.stopbits = 1     # Number of Stop bits = 1
SerialObj.write(b'VLS 10\n')
SerialObj.write(('MOV U '+str(10)+' V '+str(3)+'\n').encode('ascii'))
time.sleep(.5)
SerialObj.write(('MOV U '+str(0)+' V '+str(0)+'\n').encode('ascii'))
SerialObj.close()