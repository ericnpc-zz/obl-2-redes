from socket import *
import threading

serverPort = 2020
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('El servidor esta listo para recibir')

while True: 
	connectionSocket, addr = serverSocket.accept()
	t = threading.Thread(target=sendFile, args=['asdasd', connectionSocket])
	t.start()
	# sentence = connectionSocket.recv(1024).decode()
	# capitalizedSentence = sentence.upper()


def sendFile(fileName, connectionSocket):
	file_to_send = open(fileName, 'rb')
	file_data = file_to_send.read(400000) #buffer de cuantos bytes va a leer (creo)
	connectionSocket.send(file_data)
	connectionSocket.close()