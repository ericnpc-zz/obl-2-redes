from socket import *

serverPort = 2020
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((gethostname(), serverPort))
serverSocket.listen(1)
print('El servidor esta listo para recibir')
while True: 
	connectionSocket, addr = serverSocket.accept()
	# sentence = connectionSocket.recv(1024).decode()
	# capitalizedSentence = sentence.upper()
	file_to_send = open(r"/Users/petterboussard/Documents/obl-2-redes/holis.txt", 'rb')
	file_data = file_to_send.read(400000)
	connectionSocket.send(file_data)
	connectionSocket.close()
