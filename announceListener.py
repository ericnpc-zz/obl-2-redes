from socket import *
from datetime import datetime
import fileRepository

BUFFER_SIZE = 65536

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
		message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
		print('received message: ', message)
		while message:
			# if clientAddress
			handleAnnouncement(message, clientAddress)
			message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
			print('received message within while: ', message)
			
		# serverSocket.sendto(message.encode(), clientAddress)

def handleAnnouncement(message, clientAddress):
	print('----> message antes del split: ', message)
	messageArray = message.split('\n')
	messageType = messageArray[0]
	print('Message Type: ', messageType)
	messageElements = messageArray[1:]
	messageElements.pop(len(messageElements)-1)
	print('Message Elements: ', messageElements)

	if messageType == 'ANNOUNCE':

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

			# for md5 in _remoteFiles.keys():
			# 	file = _remoteFiles[md5]
			# 	for host in file['hosts']:
			# 		if (datetime.now() - host['lastAnnounced']).seconds >= 90:
			# 			file['hosts'].remove(host)

		fileRepository.setRemoteFiles(_remoteFiles)

		aa = fileRepository.getRemoteFiles()
		print('Remote files updated: ', aa)
	elif messageType == 'REQUEST':
		print('REQUEST')

def forceClose():
	global serverSocket
	serverSocket.close()
	print('Announce Listener Socket Closed')


