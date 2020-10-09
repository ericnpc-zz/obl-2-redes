from socket import *

import re
import main

COMMAND_EXIT = 'exit'
COMMAND_LIST = 'list'
COMMAND_OFFER = 'offer'
COMMAND_GET = 'get'

serverPort = 2026
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((gethostbyname(gethostname()), serverPort))
serverSocket.listen(1)

print('The telnet server is ready to receive commands')

connectionSocket, addr = serverSocket.accept()

while True: 
	command = connectionSocket.recv(2048).decode().strip().lower()
	print(command)

	# capitalizedSentence = sentence.upper()
	if command == COMMAND_LIST:
		remoteFiles = main.listRemoteFiles()
		connectionSocket.send(remoteFiles)

	elif re.match("get .*", command):
		fileId = command.split('get ')[1]
		main.getFile(fileId)
		print(fileId)

	elif re.match("offer .*", command):
		path = command.split('offer ')[1]
		l = main.offerFile(path)
		# print(l[0]['fileName'])

	elif command == COMMAND_EXIT:
		print('bye')
		connectionSocket.send(addr + ' ')
		connectionSocket.close()
		serverSocket.close()
