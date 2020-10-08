from socket import *
import ipaddress

IP = unicode(gethostbyname(gethostname()))
MASK = unicode('255.255.255.0')

serverPort = 2020
clientSocket = socket(AF_INET, SOCK_DGRAM)

net = ipaddress.IPv4Network(IP + '/' + MASK, False)
print('Broadcast:', net.broadcast_address)

message = raw_input("Escriba una frase en minusculas:")
# message = "<ANNOUNCE\n<mulan.mkv>\t<11961255187>\t<>"
print(message)
clientSocket.sendto(message.encode(),(net.broadcast_address, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()