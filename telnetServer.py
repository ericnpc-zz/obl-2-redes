from socket import *

import re
# import main

COMMAND_EXIT = 'exit'
COMMAND_LIST = 'list'
COMMAND_OFFER = 'offer'
COMMAND_GET = 'get'

serverPort = 2026
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# string vacio porque https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets/16130819
serverSocket.listen(1)

print('The telnet server is ready to receive commands')

while True:
	connectionSocket, addr = serverSocket.accept()
	exit = False
	while not exit: 
		command = connectionSocket.recv(2048).decode().strip().lower()
		print(command)

		if command == COMMAND_LIST:
			# remoteFiles = main.listRemoteFiles()
			# connectionSocket.send(remoteFiles)
			connectionSocket.send("hola")

		elif re.match("get .*", command):
			# fileId = command.split('get ')[1]
			# main.getFile(fileId)
			# print(fileId)
			connectionSocket.send("hola")

		elif re.match("offer .*", command):
			path = command.split('offer ')[1]
			l = main.offerFile(path)
			# print(l[0]['fileName'])

		elif command == COMMAND_EXIT:
			print('bye')
			# connectionSocket.send(addr + ' ')
			connectionSocket.close()
			# serverSocket.close()
			exit = True
