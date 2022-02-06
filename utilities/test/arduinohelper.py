import serial
import time
import os

s = serial.Serial(port= '/dev/ttyACM0', baudrate= 9600)
dirPath= os.getcwd()

#print(open(dirPath + '/ard.txt', 'r').read())
while True:
    try:
        with open(dirPath + '/ard.txt', 'r') as msg:
            m= msg.read()
            cmd= None

            if 'on' in m: cmd= 'on'
            elif 'off' in m: cmd= 'off'

            s.write('{}'.format(cmd).encode())
            print(m)
        os.remove(dirPath + '/ard.txt')

    except Exception:
        print(Exception)
