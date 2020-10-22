from socket import *
import threading

BUFFER_SIZE = 4096

def sendFile(clientSocket):
	messageFromDownloader = clientSocket.recv(4096)
	messageFromDownloader = messageFromDownloader.split('\n')[1:]

	print(messageFromDownloader)

	md5, start, size = messageFromDownloader

	file_to_send = open("/Users/petterboussard/Documents/asd.mp4", 'rb')
	file_to_send.seek(int(start))

	bytes_to_send = int(size)
	header = "DOWNLOAD OK\n"
	file_data = header + file_to_send.read(min(BUFFER_SIZE, bytes_to_send))

	while (file_data and bytes_to_send > 0):
		clientSocket.send(file_data)
		bytes_to_send = bytes_to_send - BUFFER_SIZE
		file_data = file_to_send.read(min(BUFFER_SIZE, bytes_to_send))

	clientSocket.close()

def fileSender():
	serverPort = 2031
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', serverPort))
	serverSocket.listen(1)

	print('El servidor esta listo para recibir pedidos')

	while True: 
		clientSocket, addr = serverSocket.accept()
		print('conexion aceptada')
		t = threading.Thread(target=sendFile, args=[clientSocket])
		t.start()

fileSender()