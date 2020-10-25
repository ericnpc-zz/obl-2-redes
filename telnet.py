from socket import *
import utils_file_input
import re
import fileDownloader
import fileRepository
import os

global serverSocket

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
		fileId = fileId + 1
		fileIdtoMD5[fileId] = md5
		remoteFilesString = remoteFilesString + str(fileId) + "\t" + str(file["size"]) + "\t" + fileNames + "\n"

	return remoteFilesString, fileIdtoMD5

def telnetServer():
	COMMAND_EXIT = 'exit'
	COMMAND_LIST = 'list'
	LIST_OFFERED = 'list offered'

	remoteFileListOfMD5 = []
	remoteFiles = {}

	serverPort = 2028
	global serverSocket
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #para poder reutilizar la address luego de cerrar el programa

	serverSocket.bind(('', serverPort))
	# string vacio porque https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets/16130819
	serverSocket.listen(0)

	print('The telnet server is ready to receive commands')

	while True:
		clientSocket, addr = serverSocket.accept()

		welcomeMessage = '\n\nCOMMANDS AVAILABLE:\n\n'
		welcomeMessage = welcomeMessage + '- list \t(will list files available for download)\n'
		welcomeMessage = welcomeMessage + '- get <id> (will download the remote file with the specified id)\n'
		welcomeMessage = welcomeMessage + '- list offered (will list files offered by you)\n'
		welcomeMessage = welcomeMessage + '- offer <path> (will offer the file specified in <path>)\n'
		welcomeMessage = welcomeMessage + '- exit \t(will close the program)\n\n'

		clientSocket.send(welcomeMessage)

		exit = False
		while not exit: 
			command = clientSocket.recv(2048).decode().strip().lower()
			print(command)

			if command == COMMAND_LIST:
				remoteFilesString, remoteFileListOfMD5 = listRemoteFiles()
				print(remoteFileListOfMD5)
				if remoteFilesString != '':
					remoteFilesString = 'FILES AVAILABLE:\n\nId\tSize\t\tNames\n' + remoteFilesString
				else: 
					remoteFilesString = 'NO FILES AVAILABLE\n\n'
				clientSocket.send(remoteFilesString)				

			elif re.match("get .*", command):
				clientSocket.send("Downloading...\n")
				fileId = command.split('get ')[1]
				print(remoteFileListOfMD5)
				print(fileId)
				print(int(fileId))
				if remoteFileListOfMD5.has_key(fileId):
					fileMD5 = remoteFileListOfMD5[int(fileId)]

					fileMetadata = fileRepository.getRemoteFile(fileMD5)

					fileMissing = False

					if fileMetadata == {}:
						downloadStatus = False
						fileMissing = True
					else:
						downloadStatus, error = fileDownloader.download(fileMD5, fileMetadata)

					if downloadStatus:
						msg = "Download Success"
					else:
						if fileMissing:
							msg = "File no longer available"
						else:
							msg = "Download Failed, try again, error: " + error
					clientSocket.send(msg + "\n")
				else:
					clientSocket.send("Please enter a valid id\n\n")

			elif re.match("offer .*", command):
				path = command.split('offer ')[1].replace('\\','') #agregue esto para soportar archivos con espacios en el nombre
				l = offerFile(path)
				clientSocket.send("File offered successfully\n")

			elif command == LIST_OFFERED:
				localFiles = fileRepository.getLocalFiles()
				localFilesString = ''
				if len(localFiles) > 0:
					for file in localFiles:
						localFilesString += 'FILES CURRENTLY BEING OFFERED: \n\nName\tSize\tMD5\n'
						localFilesString += file['fileName'] + '\t' + str(file['size']) + '\t' + file['md5'] + '\n'
				else:
					localFilesString = 'NO FILES BEING OFFERED\n\n'
				clientSocket.send(localFilesString)
				
			elif command == COMMAND_EXIT:
				print('Closing connection. Bye!\n\n')
				clientSocket.close()
				exit = True

# TODO: Borrar si no sirve - junto con los globals
def forceClose():
	global serverSocket
	serverSocket.close()
	print('Telnet Socket Closed')