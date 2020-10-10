from socket import *
import main #borrar despues
import utils_file_input
import time
import random


def initializeClient(): 
    serverPort = 2020
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while True:
        message = utils_file_input.announce(main.localFiles)
        print(message)

        clientSocket.sendto(message.encode(),('<broadcast>', serverPort))

        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())

        time.sleep(5 + random.random()) # TODO: Tiene que ser 30 segs

    clientSocket.close()