from socket import *
import utils_file_input
import re
import fileDownloader
import os

def telnetServer():
	global mainObj
	COMMAND_EXIT = 'exit'
	COMMAND_LIST = 'list'

	remoteFileListOfMD5 = []
	remoteFiles = {}

	serverPort = 2023
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', serverPort))
	# string vacio porque https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets/16130819
	serverSocket.listen(0)

	print('The telnet server is ready to receive commands')

	while True:
		clientSocket, addr = serverSocket.accept()
		exit = False
		while not exit: 
			command = clientSocket.recv(2048).decode().strip().lower()
			print(command)

			if command == COMMAND_LIST:
				remoteFiles = main.listRemoteFiles()
				remoteFileListOfMD5 = remoteFiles.keys()
				files = utils_file_input.getFileListDescription(remoteFiles)
				# popular la lista local de indices->md5
				print(remoteFileListOfMD5)
				clientSocket.send(files)

			elif re.match("get .*", command):
				fileId = command.split('get ')[1]
				fileMD5 = remoteFileListOfMD5[int(fileId) - 1] 
				fileDownloader.prepareForDownload(fileMD5)
				# main.getFile(fileId)
				# if remoteFileList
				# manejar el caso en que la lista sea null
				clientSocket.send("hola")

			elif re.match("offer .*", command):
				path = command.split('offer ')[1]
				l = mainObj.offerFile(path)
				print(l)
				clientSocket.send("File offered successfully\n")

			elif command == COMMAND_EXIT:
				print('bye')
				# clientSocket.send(addr + ' ')
				clientSocket.close()
				# serverSocket.close()
				exit = True
