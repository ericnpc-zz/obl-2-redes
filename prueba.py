from socket import *
import os
import re
import sys

global serverSocket

COMMAND_EXIT = 'exit'
COMMAND_LIST = 'list'

remoteFileListOfMD5 = []
remoteFiles = {}

serverPort = 20291
global serverSocket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Justificar que hace TODO

try:
    serverSocket.bind(('', serverPort))
except:
    print("ERROR ", sys.exc_info())
# string vacio porque https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets/16130819
serverSocket.listen(0)

print('The telnet server is ready to receive commands')
clientSocket, addr = serverSocket.accept()

while True:
    command = clientSocket.recv(2048).decode().strip().lower()
    print(command)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if command == COMMAND_LIST:
        remoteFilesString, remoteFileListOfMD5 = listRemoteFiles()
        print(remoteFileListOfMD5)
        clientSocket.send(remoteFilesString)				

    elif re.match("get .*", command):
        clientSocket.send("Downloading...\n")
        fileId = command.split('get ')[1]
        print(remoteFileListOfMD5)
        print(fileId)
        print(int(fileId))
        fileMD5 = remoteFileListOfMD5[int(fileId)]

        fileMetadata = fileRepository.getRemoteFile(fileMD5)

        fileMissing = False

        if fileMetadata == {}:
            downloadStatus = False
            fileMissing = True
        else:
            downloadStatus, error = fileDownloader.download(fileMD5, fileMetadata)

        if downloadStatus:
            msg = "Download Success"
        else:
            if fileMissing:
                msg = "File no longer available"
            else:
                msg = "Download Failed, try again, error: " + error
        clientSocket.send(msg + "\n")
    elif command == COMMAND_EXIT:
        print("OK")
        print(chr(27) + "[2J")
        print("OK")
    