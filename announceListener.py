from socket import *
from datetime import datetime
from threading import Thread
import fileRepository
import announceSender
import time
import random

BUFFER_SIZE = 65536

global serverSocket
shouldCheckAvailability = True

# Esta funcion va a ser llamada desde el thread que se inicia junto con el programa
# principal. Escucha permanentemente mensajes de tipo ANNOUNCE y REQUEST.
def startListening():
	serverPort = 2020
	global serverSocket
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	ip  = serverSocket.getsockname()[0]
	serverSocket.bind(('', serverPort))

	# Obtengo mi direccion ip local 
	# para ignorar mis propios anuncios
	s = socket(AF_INET, SOCK_DGRAM)
	s.connect(('8.8.8.8',53))
	myIp = s.getsockname()[0]
	s.close()

	print("[announceListener.startListening] El announceListener esta listo para recibir\n")

	while True:
		message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
		while message:
			if clientAddress[0] != myIp:
				handleAnnouncement(message, clientAddress, serverSocket)
			message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
			

# Procesa los mensajes recibidos dentro de la funcion startListening. 
# En caso de ser ANNOUNCEs, actualiza la lista de remotes files y de ser REQUEST
# se envia un mensaje ANNOUNCE forzadamente al host que lo solicito.
def handleAnnouncement(message, clientAddress, serverSocket):

	messageArray = message.split('\n')
	messageType = messageArray[0]
	print('[announceListener.handleAnnouncement] Message Type: ', messageType + '\n')
	messageElements = messageArray[1:]

	if messageType == 'ANNOUNCE':
		messageElements.pop(len(messageElements)-1)
		print('[announceListener.handleAnnouncement] Announce Message Elements: ', messageElements + '\n')

		_remoteFiles = fileRepository.getRemoteFiles()

		if len(messageElements) > 0:
			for elem in messageElements:
				data = elem.split('\t')
				fileName = data[0]
				fileSize = data[1]
				fileMD5 = data[2]

				if _remoteFiles.has_key(fileMD5):
					file = _remoteFiles[fileMD5]

					isPresent = False
					for host in file['hosts']:
						if host['ip'] == clientAddress[0]:
							isPresent = True
							host['lastAnnounced'] = datetime.now()

					if not isPresent:
						file['hosts'].append({
							'ip': clientAddress[0],
							'name': fileName,
							'lastAnnounced': datetime.now()
						})		
				else: 
					_remoteFiles[fileMD5] = {
						'size': int(fileSize),
						'hosts': [{
							'ip': clientAddress[0],
							'name': fileName,
							'lastAnnounced': datetime.now()
						}]
					}

		fileRepository.setRemoteFiles(_remoteFiles)

	elif messageType == 'REQUEST':
		# Mandamos el ANNOUNCE forzado
		Thread(target=announceSender.sendAnnounceMessages, args=[serverSocket, clientAddress[0]]).start()

# Esta funcion va a correr permanentemente en un thread abierto desde el programa principal
# Corrobora los time stamps de cada archivo ofrecido por cada host para quitar de la lista
# aquellos que hayan sido ofrecidos por ultima vez hace mas de 90 segundos.
def checkAvailability():
	global shouldCheckAvailability
	while shouldCheckAvailability:
		_remoteFiles = fileRepository.getRemoteFiles()

		for md5 in _remoteFiles.keys():
			file = _remoteFiles[md5]
			for host in file['hosts']:
				if (datetime.now() - host['lastAnnounced']).seconds >= 90:
					file['hosts'].remove(host)
					if len(file['hosts']) == 0:
						_remoteFiles.pop(md5)


		fileRepository.setRemoteFiles(_remoteFiles)
		print('[announceListener.checkAvailability] Current remote files: ' + str(_remoteFiles))
		time.sleep(30)

# Cierra sockets y evita la continuacion de las tareas en caso de haber ocurrido un ctrl+c.
def forceClose():
	global serverSocket
	serverSocket.close()
	global shouldCheckAvailability
	shouldCheckAvailability = False
	print('[announceListener.forceClose] Announce Listener Socket Closed\n')
