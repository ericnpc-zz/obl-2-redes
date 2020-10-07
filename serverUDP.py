from socket import *
serverPort = 2020
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((gethostname(), serverPort))
print("El servidor esta listo para recibir")
while True:
  message, clientAddress = serverSocket.recvfrom(2048)
  print(message)
  print(clientAddress)
  modifiedMessage = message.decode().upper()
  print(modifiedMessage)
  serverSocket.sendto(modifiedMessage.encode(), clientAddress)



# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serverPort = 1234
# s.bind((socket.gethostname(), 1234))
# s.listen(5)

# while True:
#   clientSocket, address = s.accept()
#   print("Connection from {address} has been established!")
#   clientSocket.send(bytes("Welcome to the server!", "utf-8"))

