from socket import *
from threading import Thread
import os

def prepareForDownload(fileMD5, fileMetadata): 
	size = fileMetadata['size']
	hosts = fileMetadata['hosts']
	packetSize = size / len(hosts)
	packetRemain = size % len(hosts)
	fileName = os.path.split(fileMetadata['hosts'][0]['name'])[1:][0]

	threads = []
	
	for i in range(len(hosts)):
		size = packetSize
		host = hosts[i]
		if i == len(hosts) - 1 :
			size = size + packetRemain 
		start = i * packetSize

		# print(str(start) + "\n" + str(size) + "\n")
		# print("*******")
		# print(start, size)

		t = Thread(target=downloadViaTCP, args=[host['ip'], size, start, fileMD5, fileName + '.part' + str(i)])
		t.start()
		threads.append(t)
	
	for thread in threads:
		print('//////////////////\n Joining Thread\n/////////////////\n')
		thread.join()
	
	final_file = open('ARCHIVO_RECIBIDO.mp4', 'wb')

	for i in range(len(hosts)):
		file_part = open(fileName + '.part' + str(i), 'rb')
		file_data = file_part.read(4096)
		final_file.write(file_data)
		while (file_data):
			file_data = file_part.read(4096)
			final_file.write(file_data)

		file_part.close()
		#tenemos que borrar los archivos temporales
	final_file.close()


def downloadViaTCP(hostIP, size, start, md5, fileName):
	print('//////////////////\n' + 'Downloading from ' + str(hostIP) + '\n//////////////////\n\n')
    
	serverPort = 2030
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((hostIP, serverPort))

	downloadMessage = "DOWNLOAD\n" + md5 + "\n" + str(start) + "\n" + str(size)
	clientSocket.send(downloadMessage.encode())

	received_file = open(fileName,'wb')
	file_data_from_server = clientSocket.recv(4096)
	print("tamano recibido en el primer paquete",len(file_data_from_server))
	# print('#############' + str(start))
	# print(file_data_from_server)
	# print('#############')
	file_data_from_server = file_data_from_server.split('DOWNLOAD OK\n')
	# print(file_data_from_server)
	file_data_from_server = file_data_from_server[1]
	while (file_data_from_server):
		received_file.write(file_data_from_server)
		print("before receive")
		file_data_from_server = clientSocket.recv(4096)
		print("tamano recibido dentro del while",len(file_data_from_server))

		print("after receive")


	received_file.close()
	clientSocket.close()

remoteFiles = {}

remoteFiles['a']= {
        'size': 38173178,
        'hosts': [ 
        			{'ip': 'localhost',
                    'name': 'nombre_random',
                    'lastAnnounced': 'fecha'
                    }, 
                    {'ip': '10.0.1.133',
                     'name': 'perrito',
                     'lastAnnounced': 'fecha'
                    }
                  ]     
}

fileMD5 = 'a'
fileMetadata = remoteFiles[fileMD5]
prepareForDownload(fileMD5, fileMetadata)