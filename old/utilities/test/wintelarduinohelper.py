import serial
import time
import os
import subprocess
import lightcipher

dirPath= os.getcwd()

c1bMax= True
c2bMax= True
i= 0
while True:
    try:
        if i == 0: s = serial.Serial(port= '/dev/ttyACM0', baudrate= 9600)
        elif i == 1: s = serial.Serial(port= '/dev/ttyACM1', baudrate= 9600)
        else:
            print('No device was found.')
        break
    except Exception:
        print(Exception)
        i+= 1
    else:
        while True:
            try:
                file = open(dirPath + '/ard1.txt')
                file.close()
                os.remove(dirPath + '/ard1.txt')

            except Exception:
                #print(Exception)
                pass

            else:
                execute= ""
                extra= ""
                msg= open(dirPath + '/ard.txt')
                m= msg.read()

                # Special commands.
                if 'exit' in m:
                    print('Refreshing scripts:')
                    subprocess.call(dirPath + '/RunLights.sh')
                elif 'lock' in m:
                    print('Locking up.')
                    execute+= 'r3 2,'
                    execute+= 'r3 3,'
                elif 'movie' in m:
                    execute+='r2 5,'
                    execute+='r1 15,'
                    execute+='r1 2,'
                    c1bMax= False
                elif 'happy' in m:
                    execute+='r2 15,'
                    execute+='r1 13,'

                else:
                    execute= lightcipher.cipher(m)

                # Resets the brightness of lights.
                if not c1bMax and 'movie' not in m:
                    extra+='r1 1,'
                    c1bMax= True
                if not c2bMax:
                    extra+='r2 1,'
                    c2bMax= True

                print(extra)
                print(execute)
                if extra:
                    s.write('{}'.format(extra).encode())
                    time.sleep(3)
                s.write('{}'.format(execute).encode())
                time.sleep(5)
                s.write(b'stop,')
