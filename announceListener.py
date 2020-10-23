from socket import *

global serverSocket

def startListening():

	serverPort = 2020
	global serverSocket
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	# serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	serverSocket.bind(('', serverPort))
	print("El announceListener esta listo para recibir")

	# announcesInProgress = {
	# 	ip: [paquetes] # cuando se terminen se descartan - podemos usar seq_numbers y tambien timestamps y timeouts
	# }

	storedAnnounces = {}

	def addAnnouncement(ip, payload):
		if ip in storedAnnounces:
			announceForIp = storedAnnounces[ip]
			if not payload in announceForIp:
				storedAnnounces[ip].append(payload)
		else:
			storedAnnounces[ip] = [payload]
		print(storedAnnounces)

	while True:
		message, clientAddress = serverSocket.recvfrom(4096)
		# fullMessage = ''
		# print('received message: ', message)
		# while message:
		# 	fullMessage = fullMessage + str(message)
		# 	message = serverSocket.recvfrom(4096)
		# 	print('received message: ', message)

		addAnnouncement(clientAddress, message)
		#print(message)
		# handleAnnouncement()
		# serverSocket.sendto(message.encode(), clientAddress)

	# def handleAnnouncement:

def forceClose():
	global serverSocket
	serverSocket.close()
	print('Announce Listener Socket Closed')


	