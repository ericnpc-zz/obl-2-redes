import utils_file_input
from threading import Thread, Lock
from datetime import datetime
# import telnet
from socket import *
import utils_file_input
import re
import fileDownloader
import os

# class main():

    # Manejo de Archivos y Concurrencia de Acceso

remoteFiles = {}
localFiles = []

localFileLock = Lock()
remoteFileLock = Lock()

def getLocalFile(index):
    localFileLock.acquire()
    _localFile = localFiles(index).copy()
    localFileLock.release()
    return _localFile

def setLocalFile(localFile):
    localFileLock.acquire()
    localFiles.append(localFile)
    localFileLock.release()

def getRemoteFile(md5):
    remoteFileLock.acquire()
    _remoteFile = remoteFiles[md5].copy()
    remoteFileLock.release()
    return _remoteFile

def getRemoteFiles():
    remoteFileLock.acquire()
    _remoteFiles = remoteFiles.copy()
    remoteFileLock.release()
    return _remoteFiles

def setRemoteFile(md5, value):
    remoteFileLock.acquire()
    remoteFiles[md5] = value
    remoteFileLock.release()

def deleteRemoteFile(md5):
    remoteFileLock.acquire()
    remoteFiles.pop(md5)
    remoteFileLock.release()

# localFiles.append({
# 	'fileName': 'pepito.js',
# 	'size': 203859400,
# 	'md5': 'hdaksehqi378437n73qkay3874q3'
# })

remoteFiles['hdaksehqi378437n73qkay3874q']= {
        'size': 38173178,
        'hosts': [ {'ip': 'localhost',
                    'name': 'nombre_random.ext',
                    'lastAnnounced': datetime.now()
                    }, 
                    {'ip': '10.0.1.133',
                      'name': 'perrito.ext',
                     'lastAnnounced': datetime.now()
                    }
                  ]        
}


def listRemoteFiles():
    remoteFilesString = ''
    fileId = 0
    remoteFiles = getRemoteFiles()

    fileIdtoMD5 = {}

    for md5 in remoteFiles.keys():
        file = remoteFiles[md5]
        fileNames = ''
        for host in file['hosts']:
            fileNames += host['name'] + ", "
        fileId =+ 1
        fileIdtoMD5[fileId] = md5

        remoteFilesString = remoteFilesString + str(fileId) + "\t" + str(file["size"]) + "\t" + fileNames + "\n"
    return remoteFilesString, fileIdtoMD5


def offerFile(path):

    _md5 = utils_file_input.md5(path)
    _size = utils_file_input.size(path)

    elem = {
        "md5": _md5,
        "size": _size,
        "fileName": path
    }

    setLocalFile(elem)


    return localFiles

def getFile(fileMD5):
    file = file


def telnetServer():
    COMMAND_EXIT = 'exit'
    COMMAND_LIST = 'list'

    remoteFileListOfMD5 = []
    remoteFiles = {}

    serverPort = 2036
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    # string vacio porque https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets/16130819
    serverSocket.listen(0)

    print('The telnet server is ready to receive commands')

    while True:
        clientSocket, addr = serverSocket.accept()
        exit = False
        while not exit: 
            command = clientSocket.recv(2048).decode().strip().lower()
            print(command)

            if command == COMMAND_LIST:
                remoteFilesString, remoteFileListOfMD5 = listRemoteFiles()
                print(remoteFileListOfMD5)
                clientSocket.send(remoteFilesString)

            elif re.match("get .*", command):
                fileId = command.split('get ')[1]
                print(remoteFileListOfMD5)
                print(fileId)
                print(int(fileId))
                fileMD5 = remoteFileListOfMD5[int(fileId)]

                prepareForDownload(fileMD5, getRemoteFile(fileMD5))
                # main.getFile(fileId)
                # if remoteFileList
                # manejar el caso en que la lista sea null
                clientSocket.send("archivo descargado, chau")

            elif re.match("offer .*", command):
                path = command.split('offer ')[1]
                l = offerFile(path)
                print(l)
                clientSocket.send("File offered successfully\n")

            elif command == COMMAND_EXIT:
                print('bye')
                # clientSocket.send(addr + ' ')
                clientSocket.close()
                # serverSocket.close()
                exit = True

########################### EMPIEZA fileSender

BUFFER_SIZE = 4096

def sendFile(clientSocket):
    messageFromDownloader = clientSocket.recv(4096)
    messageFromDownloader = messageFromDownloader.split('\n')[1:]

    print(messageFromDownloader)

    md5, start, size = messageFromDownloader

    file_to_send = open("/Users/petterboussard/Documents/asd.mp4", 'rb')
    file_to_send.seek(int(start))

    bytes_to_send = int(size)
    header = "DOWNLOAD OK\n"
    file_data = header + file_to_send.read(min(BUFFER_SIZE, bytes_to_send))

    while (file_data and bytes_to_send > 0):
        clientSocket.send(file_data)
        bytes_to_send = bytes_to_send - BUFFER_SIZE
        file_data = file_to_send.read(min(BUFFER_SIZE, bytes_to_send))

    clientSocket.close()

def fileSender():
    serverPort = 2030
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)

    print('El servidor esta listo para recibir pedidos')

    while True: 
        clientSocket, addr = serverSocket.accept()
        print('conexion aceptada')
        t = Thread(target=sendFile, args=[clientSocket])
        t.start()

########################## TERMINA fileSender

def prepareForDownload(fileMD5, fileMetadata): 
    size = fileMetadata['size']
    hosts = fileMetadata['hosts']
    packetSize = size / len(hosts)
    packetRemain = size % len(hosts)
    fileName = os.path.split(fileMetadata['hosts'][0]['name'])[1:][0]

    threads = []
    
    for i in range(len(hosts)):
        size = packetSize
        host = hosts[i]
        if i == len(hosts) - 1 :
            size = size + packetRemain 
        start = i * packetSize

        # print(str(start) + "\n" + str(size) + "\n")
        # print("*******")
        # print(start, size)

        t = Thread(target=downloadViaTCP, args=[host['ip'], size, start, fileMD5, fileName + '.part' + str(i)])
        t.start()
        threads.append(t)
    
    for thread in threads:
        print('//////////////////\n Joining Thread\n/////////////////\n')
        thread.join()
    
    final_file = open(fileName, 'wb')

    for i in range(len(hosts)):
        file_part = open(fileName + '.part' + str(i), 'rb')
        file_data = file_part.read(4096)
        final_file.write(file_data)
        while (file_data):
            file_data = file_part.read(4096)
            final_file.write(file_data)

        file_part.close()
        os.remove(fileName + '.part' + str(i))
        #tenemos que borrar los archivos temporales
    final_file.close()

    print("MD5 Check: ", utils_file_input.md5(fileName) == fileMD5)


def downloadViaTCP(hostIP, size, start, md5, fileName):
    print('//////////////////\n' + 'Downloading from ' + str(hostIP) + '\n//////////////////\n\n')
    
    serverPort = 2030
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((hostIP, serverPort))

    downloadMessage = "DOWNLOAD\n" + md5 + "\n" + str(start) + "\n" + str(size)
    clientSocket.send(downloadMessage.encode())

    received_file = open(fileName,'wb')
    file_data_from_server = clientSocket.recv(4096)
    print("tamano recibido en el primer paquete",len(file_data_from_server))
    # print('#############' + str(start))
    # print(file_data_from_server)
    # print('#############')
    file_data_from_server = file_data_from_server.split('DOWNLOAD OK\n')
    # print(file_data_from_server)
    file_data_from_server = file_data_from_server[1]
    while (file_data_from_server):
        received_file.write(file_data_from_server)
        print("before receive")
        file_data_from_server = clientSocket.recv(4096)
        print("tamano recibido dentro del while",len(file_data_from_server))

        print("after receive")


    received_file.close()
    clientSocket.close()

######################### TERMINA fileDownloader

# global mainObj
# mainObj = main()

telnetThread = Thread(target=telnetServer)

telnetThread.start()

fileSenderThread = Thread(target=fileSender)

fileSenderThread.start()


# telnetCliThread = telnetThread()
# telnetCliThread.start()


# MAIN2
# # inicializo thread con lista
# announceThread = announcesThread(fileList)
# announceThread.start()

# # capturo seleccion del usuario
# md5 = captureUserSelection(fileList)

# if md5 == "":
#     print("\nAborto Exitoso\n")
# else:
#     print("\nDescargando el archivo con MD5: " + md5)

# # actualizando lista de archivos del thread
# newFileList = {}
# newFileList["TUVIEJA"] = dict1
# announceThread.setFileList(newFileList)