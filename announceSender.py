from socket import *
import utils_file_input
import time
import random

def startSending(): 
	serverPort = 2020
	clientSocket = socket(AF_INET, SOCK_DGRAM)

	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #aca comentar bien que son estas options o properties que estmos seteando
	clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	while True:

		message = utils_file_input.getAnnounceMessage()
		print("Announce message about to be sent: ", message)



		clientSocket.sendto(message.encode(),('<broadcast>', serverPort))

		# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
		# print(modifiedMessage.decode())

		time.sleep(5 + random.random()) # TODO: Tiene que ser 30 segs

	clientSocket.close()