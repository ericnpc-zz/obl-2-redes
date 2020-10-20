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
		if i == len(hosts)-1:
			size =+ packetRemain 

		start = i * packetSize
		# print('host' + host)
		# print('size' + str(size))
		# print('start' + str(start))
		# print(fileMD5)
		# print(fileName)
		t = Thread(target=downloadViaTCP, args=[host['ip'], size, start, fileMD5, fileName + '.part' + str(i)])
		t.start()
		threads.append(t)
	
	for thread in threads:
		print('//////////////////\n Joining Thread\n/////////////////\n')
		thread.join()
	
	final_file = open(fileName, 'wb')

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
    
	serverPort = 2031
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((hostIP, serverPort))

	received_file = open(fileName,'wb')
	file_data_from_server = clientSocket.recv(4096)
	while (file_data_from_server):
		received_file.write(file_data_from_server)
		file_data_from_server = clientSocket.recv(4096)

	received_file.close()
	clientSocket.close()

remoteFiles = {}

remoteFiles['hdaksehqi378437n73qkay3874q']= {
        'size': 61311584,
        'hosts': [ {'ip': 'localhost',
                    'name': '/Users/nadiarecarey/Desktop/Screen Recording 2020-10-14 at 7.21.45 PM.mov'
                    # 'lastAnnounced': datetime.now()
                    # }, 
                    # {'ip': '192.168.1.2',
                    #  'name': 'perrito.js'
                    # #  'lastAnnounced': datetime.now()
                    }
                  ]        
}
fileMD5 = 'hdaksehqi378437n73qkay3874q'
fileMetadata = remoteFiles[fileMD5]
prepareForDownload(fileMD5, fileMetadata)