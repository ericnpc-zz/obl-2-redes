from socket import *

def prepareForDownload(fileMD5): 
	size = remoteFiles[fileMD5]['size']
	hosts = remoteFiles[fileMD5]['hostIPs']
	packetSize = size / len(hosts)
	packetRemain = size % len(hosts)
	fileName = os.path.split(remoteFiles[fileMD5]['hosts'][0]['name'])
	
	for i in range(len(hosts)):
		size = packetSize
		host = hosts[i]
		print('len hosts' + str(len(hosts)-1))
		if i == len(hosts)-1:
			size =+ packetRemain 

		start = i * packetSize
		print('host' + host)
		print('size' + str(size))
		print('start' + str(start))
		print(fileMD5)
		downloadViaTCP(host, size, start, fileMD5, fileName)


def downloadViaTCP(hostIP, size, start, md5, fileName):
    
    serverPort = 2030
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((hostIP, serverPort))

    received_file = open(fileName,'wb')
    file_data_from_server = clientSocket.recv(4096)
    while (file_data_from_server):
        received_file.write(file_data_from_server)
        file_data_from_server = clientSocket.recv(4096)

    received_file.close()
    clientSocket.close()
