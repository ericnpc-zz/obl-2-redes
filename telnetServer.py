from socket import *

serverPort = 2026
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('10.0.1.121', serverPort))
serverSocket.listen(1)
print('The telnet server is ready to receive commands')
while True: 
	connectionSocket, addr = serverSocket.accept()
	command = connectionSocket.recv(2048).decode()
	print(command)
	# capitalizedSentence = sentence.upper()
	connectionSocket.send("Done")
	connectionSocket.close()