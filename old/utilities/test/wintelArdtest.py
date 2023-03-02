import serial
import time

i= 0
while True:
    try:
        if i == 0: s = serial.Serial(port= '/dev/ttyACM0', baudrate= 9600)
        elif i == 1: s = serial.Serial(port= '/dev/ttyACM1', baudrate= 9600)
        else: break
    except Exception:
        print(Exception)
        i+= 1
    else:
        while True:
            a= input('Command?: ')
            s.write('{}'.format(a).encode())
            time.sleep(2)
            s.write(b'stop')
            #s.close()
