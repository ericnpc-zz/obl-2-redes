from socket import *
import utils_file_input
import time
import random

def startSending(): 
	serverPort = 2020
	clientSocket = socket(AF_INET, SOCK_DGRAM)

	# https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ
	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
	clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	while True:

		message = utils_file_input.getAnnounceMessage()
		if message != '':
			print("Announce message about to be sent: ", message)

			clientSocket.sendto(message.encode(),('192.168.1.5', serverPort))
			# clientSocket.sendto(message.encode(),('<broadcast>', serverPort))

			# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
			# print(modifiedMessage.decode())

		time.sleep(15 + random.random()) # TODO: Tiene que ser 30 segs

	clientSocket.close()