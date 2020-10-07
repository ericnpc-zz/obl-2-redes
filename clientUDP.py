from socket import *
serverPort = 2020
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

message = raw_input("Escriba una frase en minusculas:")
print(message)
clientSocket.sendto(message.encode(),('<broadcast>', serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
