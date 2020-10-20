from socket import *

# def downloadViaTCP(hostIP, size, start, md5, fileName):
serverPort = 2030
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('10.0.1.129', serverPort))
# received_file = open(f"{fileName}.txt",'wb')
received_file = open("received_file.png",'wb')
file_data_from_server = clientSocket.recv(4096)
received_file.write(file_data_from_server)
received_file.close()
clientSocket.close()
