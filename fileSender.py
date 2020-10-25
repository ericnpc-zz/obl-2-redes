from socket import *
import threading
import fileRepository
import utils_file_input
import sys

BUFFER_SIZE = 4096

def sendFile(clientSocket):
	messageFromDownloader = clientSocket.recv(4096)
	messageFromDownloader = messageFromDownloader.split('\n')[1:]

	print(messageFromDownloader)

	md5, start, size = messageFromDownloader

	path = ''
	localFiles = fileRepository.getLocalFiles()
	for file in localFiles:
		if file['md5'] == md5:
			path = file['fileName']

	if path == '':
		missingMsg = "DOWNLOAD FAILURE\nMISSING\n"
		clientSocket.send(missingMsg)
	else:
		fileSize = utils_file_input.size(path)

		if int(start) + int(size) > int(fileSize):
			print('*************')
			print(fileSize)
			print('*************')
			badRequestMsg = "DOWNLOAD FAILURE\nBAD REQUEST\n"
			clientSocket.send(badRequestMsg)
		else:
			file_to_send = open(path, 'rb')
			file_to_send.seek(int(start))

			bytes_to_send = int(size)
			header = "DOWNLOAD OK\n"
			try: 
				file_data = header + file_to_send.read(min(BUFFER_SIZE, bytes_to_send))

				while (file_data and bytes_to_send > 0):
					clientSocket.send(file_data)
					bytes_to_send = bytes_to_send - BUFFER_SIZE
					file_data = file_to_send.read(min(BUFFER_SIZE, bytes_to_send))
			except:
				print('!!!!!!!!!!!!!! ERROR: ' + sys.exc_info()) 


	clientSocket.close()

def startListening():
	serverPort = 2030
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', serverPort))
	serverSocket.listen(1)

	print('El servidor esta listo para recibir pedidos')

	while True: 
		clientSocket, addr = serverSocket.accept()
		print('conexion aceptada')
		t = threading.Thread(target=sendFile, args=[clientSocket])
		t.start()
