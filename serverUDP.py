from socket import *
serverPort = 2020
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("El servidor esta listo para recibir")
while True:
  message, clientAddress = serverSocket.recvfrom(2048)
  print(message)
  print(clientAddress)
  modifiedMessage = message.decode().upper()
  print(modifiedMessage)
  serverSocket.sendto(modifiedMessage.encode(), clientAddress)
  