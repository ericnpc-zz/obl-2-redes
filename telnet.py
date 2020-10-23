from socket import *
import utils_file_input
import re
import fileDownloader
import fileRepository
import os

def getFile(fileMD5):
	file = file

def offerFile(path):
	_md5 = utils_file_input.md5(path)
	_size = utils_file_input.size(path)

	elem = {
		"md5": _md5,
		"size": _size,
		"fileName": path
	}

	fileRepository.setLocalFile(elem)
	return fileRepository.getLocalFiles()

def listRemoteFiles():
	remoteFilesString = ''
	fileId = 0
	remoteFiles = fileRepository.getRemoteFiles()

	fileIdtoMD5 = {}

	for md5 in remoteFiles.keys():
		file = remoteFiles[md5]
		fileNames = ''
		for host in file['hosts']:
			fileNames += host['name'] + ", "
		fileId =+ 1
		fileIdtoMD5[fileId] = md5

		remoteFilesString = remoteFilesString + str(fileId) + "\t" + str(file["size"]) + "\t" + fileNames + "\n"
	return remoteFilesString, fileIdtoMD5

def telnetServer():
	COMMAND_EXIT = 'exit'
	COMMAND_LIST = 'list'

	remoteFileListOfMD5 = []
	remoteFiles = {}

	serverPort = 2050
	serverSocket = socket(AF_INET, SOCK_STREAM)
	# serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

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
				remoteFilesString, remoteFileListOfMD5 = listRemoteFiles()
				print(remoteFileListOfMD5)
				clientSocket.send(remoteFilesString)				

			elif re.match("get .*", command):
				fileId = command.split('get ')[1]
				print(remoteFileListOfMD5)
				print(fileId)
				print(int(fileId))
				fileMD5 = remoteFileListOfMD5[int(fileId)]

				fileDownloader.prepareForDownload(fileMD5, fileRepository.getRemoteFile(fileMD5))
				# main.getFile(fileId)
				# if remoteFileList
				# manejar el caso en que la lista sea null
				clientSocket.send("archivo descargado, chau")

			elif re.match("offer .*", command):
				path = command.split('offer ')[1].replace('\\','') #agregue esto para soportar archivos con espacios en el nombre
				l = offerFile(path)
				clientSocket.send("File offered successfully\n")

			elif command == COMMAND_EXIT:
				print('bye')
				# clientSocket.send(addr + ' ')
				clientSocket.close()
				# serverSocket.close()		TODO: esto va, no?
				exit = True