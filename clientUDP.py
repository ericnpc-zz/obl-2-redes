from socket import *
serverPort = 2020
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input("Escriba una frase en minusculas:")
# message = "<ANNOUNCE\n<mulan.mkv>\t<11961255187>\t<>"
print(message)
clientSocket.sendto(message.encode(),('10.0.1.120', serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
