from lightcipher import get_command
import socket
import time
import serial
import os
import sys


class Command(list):
    def __init__(self, *commands):
        list.__init__(self, commands)


    def format(self):
        return (','.join([c for c in self if c]) + ',').encode()

def get_arduino():
    for i in range(2):
        try:
            ard= serial.Serial(port= f"/dev/ttyACM{i}", baudrate= 9600)
        except: pass
        else: return ard
    else: return None


if __name__ == '__main__':
    print("\n\n########## LIGHT CLIENT ##########")
    ard= get_arduino()
    if not ard:
        print("Device not found, exiting...")
        exit()
    else: print("Device found!")
    
    HOST, PORT= '', 1234
    s= socket.socket()
    s.bind((HOST, PORT))
    s.listen(3)
    print(f"Starting to listen on PORT: {PORT}")

    lower_bright= True
    upper_bright= True
    while True:
        conn, addr= s.accept()
        cmd= conn.recv(64).decode()
        print(f"Received command: {cmd}")

       # Special Commands
        if 'exit' in cmd:
            exit()
        elif 'update' in cmd:
            os.execv(sys.executable, [sys.executable, "lightclient.py"] + sys.argv)
        
        else: command= get_command(cmd) #Command(*lightcipher.cipher(cmd).split(','))

        # Reset light brightness
        brightness_fix= ''
        if 'brightness' not in cmd:
            if not lower_bright and 'movie' not in cmd:
                brightness_fix+= 'r1 1,'
            if not upper_bright:
                brightness_fix+= 'r2 1,'
            command= brightness_fix + command
        
        lower_bright= True if 'r1 1,' in command else (False if 'r1 2,' in command else lower_bright)
        upper_bright= True if 'r2 1,' in command else (False if 'r2 2,' in command else upper_bright)

        print(lower_bright, upper_bright)
        print(f"Execution Command: {command} | Brightness Fix: {brightness_fix}")
        
        ard.write(command.encode())
        conn.close()