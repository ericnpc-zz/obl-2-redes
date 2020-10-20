from socket import *
import threading

serverPort = 2030
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('El servidor esta listo para recibir pedidos')

def sendFile(fileName, connectionSocket):
	file_to_send = open("/Users/petterboussard/Desktop/download.png", 'rb')
	file_data = file_to_send.read(4096)
	connectionSocket.send(file_data)
	connectionSocket.close()

while True: 
	connectionSocket, addr = serverSocket.accept()
	t = threading.Thread(target=sendFile, args=['asdasd', connectionSocket])
	t.start()

