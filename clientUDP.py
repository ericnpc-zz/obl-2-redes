# from socket import *
# import ipaddress
# # import anuncios

# IP = unicode(gethostbyname(gethostname()))
# MASK = unicode('255.255.255.0')

# serverPort = 2020
# clientSocket = socket(AF_INET, SOCK_DGRAM)

# net = ipaddress.IPv4Network(IP + '/' + MASK, False)
# print('Broadcast:', net.broadcast_address)

# # # lock localFiles
# # files = list(main.localFiles)
# # # unlock localFiles

# # message = anuncios(files)

# # print(message)

# message = 'hola'

# clientSocket.sendto(message.encode(),(str(net.broadcast_address), serverPort))
# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# print(modifiedMessage.decode())

# clientSocket.close()

from socket import *
import ipaddress

IP = unicode(gethostbyname(gethostname()))
MASK = unicode('255.255.255.0')

serverPort = 2020
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

net = ipaddress.IPv4Network(IP + '/' + MASK, False)
print('Broadcast:', str(net.broadcast_address.compressed))

message = raw_input("Escriba una frase en minusculas:")
# message = "<ANNOUNCE\n<mulan.mkv>\t<11961255187>\t<>"
clientSocket.sendto(message.encode(),(str(net.broadcast_address.compressed), serverPort))
print(message)
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()