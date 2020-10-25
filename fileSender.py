from socket import *
import threading
import fileRepository
import utils
import sys

BUFFER_SIZE = 4096

# Este metodo se encarga de enviar el archivo solicitado, la cantidad de bytes y  
# desplazamiento indicados dentro del mensaje de solicitud de descarga. 
def sendFile(clientSocket):
	messageFromDownloader = clientSocket.recv(4096)
	messageFromDownloader = messageFromDownloader.split('\n')[1:]

	print('[fileSender.sendFile] Download request message: ' + messageFromDownloader + '\n')

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
		fileSize = utils.size(path)

		if int(start) + int(size) > int(fileSize):
			badRequestMsg = "DOWNLOAD FAILURE\nBAD REQUEST\n"
			clientSocket.send(badRequestMsg)
		else:
			fileToSend = open(path, 'rb')
			fileToSend.seek(int(start))

			bytesToSend = int(size)
			header = "DOWNLOAD OK\n"
			try: 
				fileData = header + fileToSend.read(min(BUFFER_SIZE, bytesToSend))

				while (fileData and bytesToSend > 0):
					clientSocket.send(fileData)
					bytesToSend = bytesToSend - BUFFER_SIZE
					fileData = fileToSend.read(min(BUFFER_SIZE, bytesToSend))
			except:
				print('[fileSender.sendFile] An error occurred: ' + sys.exc_info() + '\n')

	clientSocket.close()

# Esta funcion va a ser llamada desde un thread que se inicia junto con el programa
# principal. Escucha permanentemente mensajes de tipo DOWNLOAD, abriendo un thread por cada
# conexion establecida para realizar la descarga.
def startListening():
	serverPort = 2020
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', serverPort))
	serverSocket.listen(1)

	print('[fileSender.startListening]\t El servidor de descargas esta listo para recibir pedidos\n')

	while True: 
		clientSocket, addr = serverSocket.accept()
		print('[fileSender.startListening] Conexion aceptada para el host: ' + addr[0] + '\n')
		t = threading.Thread(target=sendFile, args=[clientSocket])
		t.start()
