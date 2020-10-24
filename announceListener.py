from socket import *
from datetime import datetime
import fileRepository
import announceSender
import time
import random

BUFFER_SIZE = 65536

global serverSocket
shouldCheckAvailability = True

def startListening():
	serverPort = 2020
	global serverSocket
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	ip  = serverSocket.getsockname()[0]
	serverSocket.bind(('', serverPort))

	#Obtengo mi direccion ip local
	s = socket(AF_INET, SOCK_DGRAM)
	s.connect(('8.8.8.8',53))
	myIp = s.getsockname()[0]
	s.close()

	print("El announceListener esta listo para recibir")

	while True:
		message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
		print('received message: ', message)
		while message:
			if clientAddress[0] != myIp:
				handleAnnouncement(message, clientAddress, serverSocket)
			message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
			print('received message within while: ', message)
			
		# serverSocket.sendto(message.encode(), clientAddress)

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
		print('checkAvailability check', _remoteFiles)
		time.sleep(30)

def handleAnnouncement(message, clientAddress, serverSocket):
	print('----> message antes del split: ', message)
	messageArray = message.split('\n')
	messageType = messageArray[0]
	print('Message Type: ', messageType)
	messageElements = messageArray[1:]
	print('Message Elements: ', messageElements)

	if messageType == 'ANNOUNCE':
		messageElements.pop(len(messageElements)-1)
		_remoteFiles = fileRepository.getRemoteFiles()
		print('_remoteFiles: ', _remoteFiles)

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
					print('^^^^^^^^^^^^^^^^^',_remoteFiles)

		fileRepository.setRemoteFiles(_remoteFiles)
		print('*********************')
		print(fileRepository.getRemoteFiles())
		print('*********************')

	elif messageType == 'REQUEST':
		#MANDAR ANNOUNCE
		time.sleep(random.randint(0, 5))
		announceSender.sendAnnounceMessages(serverSocket, clientAddress[0])

def forceClose():
	global serverSocket
	serverSocket.close()
	global shouldCheckAvailability
	shouldCheckAvailability = False
	print('Announce Listener Socket Closed')
