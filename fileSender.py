from socket import *
import threading

serverPort = 2031
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('El servidor esta listo para recibir pedidos')

def sendFile(fileName, clientSocket):
	file_to_send = open("/Users/eric/Pictures/fiestita.psd", 'rb')
	file_data = file_to_send.read(4096)
	while (file_data):
		clientSocket.send(file_data)
		file_data = file_to_send.read(4096)

	clientSocket.close()

while True: 
	clientSocket, addr = serverSocket.accept()
	print('conexion aceptada')
	t = threading.Thread(target=sendFile, args=['asdasd', clientSocket])
	t.start()