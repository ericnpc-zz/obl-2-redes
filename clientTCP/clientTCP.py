from socket import *

serverPort = 2020
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((gethostname(), serverPort))
# sentence = raw_input("Escriba una frase en minusculas:")
# clientSocket.send(sentence.encode())
# modifiedSentence = clientSocket.recv(1024)
received_file = open('received_file.txt','wb')
file_data_from_server = clientSocket.recv(400000)
received_file.write(file_data_from_server)
received_file.close()
# print("From Server: ", modifiedSentence.decode())
clientSocket.close()
