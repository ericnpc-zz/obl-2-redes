from socket import *

def downloadViaTCP(hostIP):

    serverPort = 2020
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((hostIP, serverPort))

    # clientSocket.send(sentence.encode())
    # modifiedSentence = clientSocket.recv(1024)
    received_file = open('received_file.txt','wb')
    file_data_from_server = clientSocket.recv(400000)
    received_file.write(file_data_from_server)
    received_file.close()
    # print("From Server: ", modifiedSentence.decode())
    clientSocket.close()


def getFile(fileMD5): 
    # obtener size del file y ver cuantos hosts lo ofrecen
    # dividimos el size entre hosts y lo qe sobre se loa gregamos al ultimo (lo que sobra es size mod cantHOsts)
    # for 0 to cantHosts
        # abrimos un thread para pedir el archivo, para cada host (pedimos un cacho a cada host)
        # downloadViaTCP(hostIP)
