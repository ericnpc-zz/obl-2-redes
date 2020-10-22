from socket import *

def startListening():

	serverPort = 2020
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	serverSocket.bind(('', serverPort))
	print("El announceListener esta listo para recibir")

	while True:
		message, clientAddress = serverSocket.recvfrom(2048)
		fullMessage = ''
		print('received message: ', message)
		while message:
			fullMessage = fullMessage + str(message)
			message = serverSocket.recvfrom(2048)

		print(message)
		# handleAnnouncement()
		# serverSocket.sendto(message.encode(), clientAddress)

	# def handleAnnouncement:


	