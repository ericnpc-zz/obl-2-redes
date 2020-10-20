from socket import *
# import clientUDP
import utils_file_input
import re
import main
import fileDownloader
import os

COMMAND_EXIT = 'exit'
COMMAND_LIST = 'list'
COMMAND_OFFER = 'offer'
COMMAND_GET = 'get'

remoteFileListOfMD5 = []
remoteFiles = {}

serverPort = 2023
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# string vacio porque https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets/16130819
serverSocket.listen(0)


print('The telnet server is ready to receive commands')
# clientUDP.initializeClient()

def prepareForDownload(fileMD5): 
	size = remoteFiles[fileMD5]['size']
	hosts = remoteFiles[fileMD5]['hostIPs']
	packetSize = size / len(hosts)
	packetRemain = size % len(hosts)
	fileName = os.path.split(remoteFiles[fileMD5]['hosts'][0]['name'])
	
	for i in range(len(hosts)):
		size = packetSize
		host = hosts[i]
		print('len hosts' + str(len(hosts)-1))
		if i == len(hosts)-1:
			size =+ packetRemain 

		start = i * packetSize
		print('host' + host)
		print('size' + str(size))
		print('start' + str(start))
		print(fileMD5)
		fileDownloader.downloadViaTCP(host, size, start, fileMD5, fileName)


while True:
	connectionSocket, addr = serverSocket.accept()
	exit = False
	while not exit: 
		command = connectionSocket.recv(2048).decode().strip().lower()
		print(command)

		if command == COMMAND_LIST:
			remoteFiles = main.getRemoteFiles()
			remoteFileListOfMD5 = remoteFiles.keys()
			files = utils_file_input.getFileListDescription(remoteFiles)
			# popular la lista local de indices->md5
			print(remoteFileListOfMD5)
			connectionSocket.send(files)

		elif re.match("get .*", command):
			fileId = command.split('get ')[1]
			fileMD5 = remoteFileListOfMD5[int(fileId) - 1] 
			prepareForDownload(fileMD5)
			# main.getFile(fileId)
			# if remoteFileList
			# manejar el caso en que la lista sea null
			connectionSocket.send("hola")

		elif re.match("offer .*", command):
			path = command.split('offer ')[1]
			l = main.offerFile(path)
			print(l[0]['fileName'])
			print(main.localFiles)

		elif command == COMMAND_EXIT:
			print('bye')
			# connectionSocket.send(addr + ' ')
			connectionSocket.close()
			# serverSocket.close()
			exit = True
