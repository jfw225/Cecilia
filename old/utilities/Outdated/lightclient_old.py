import socket
import time
import serial
import os
import subprocess
import lightcipher

# Define the directory path.
dirPath= os.getcwd()

# Define the light brightness status.
c1bMax= True
c2bMax= True

# Find the serial port.
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
        print('#' * 40)
        print('{:^40}'.format('Lights ready for incoming connection!'))
        print('#' * 40)

        while True:
            try:
                sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('192.168.1.19', 1234))
                m= sock.recv(50).decode()
                #s.close()

                execute= ""
                extra= ""

                # Special commands.
                if 'exit' in m:
                    print('Refreshing scripts:')
                    subprocess.call(dirPath + '/RunLights.sh')
                elif 'lock' in m:
                    print('Locking up.')
                    execute+= 'r3 2,'
                    execute+= 'r3 3,'
                elif 'home' in m:
                    print('Welcome home.')
                    execute+= 'r3 4,'
                    execute+= 'r3 1,'
                elif 'movie' in m:
                    execute+='r2 5,'
                    execute+='r1 15,'
                    execute+='r1 2,'
                    c1bMax= False
                elif 'happy' in m:
                    execute+='r2 15,'
                    execute+='r1 13,'
                elif 'sleep' in m or 'bed' in m or 'night' in m:
                    execute+= 'r2 5,'
                    execute+= 'r1 9,'
                    execute+= 'r3 2,'

                else:
                    execute= lightcipher.cipher(m)

                # Resets the brightness of lights.
                if not c1bMax and 'movie' not in m and 'brightness' not in m:
                    extra+='r1 1,'
                    c1bMax= True
                if not c2bMax and 'brightness' not in m:
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
            except Exception:
                print(Exception)

