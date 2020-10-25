from socket import *
from threading import Thread
import utils_file_input
import os
import telnet

global error
error = ''

def download(fileMD5, fileMetadata):
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

		t = Thread(target=downloadViaTCP, args=[host['ip'], size, start, fileMD5, fileName + '.part' + str(i)])
		t.start()
		threads.append(t)
	
	for thread in threads:
		print('//////////////////\n Joining Thread\n/////////////////\n')
		thread.join()

	global error
	if error != '':
		return False, error
	else:
		final_file = open(fileName, 'wb')

		for i in range(len(hosts)):
			file_part = open(fileName + '.part' + str(i), 'rb')
			file_data = file_part.read(4096)
			final_file.write(file_data)
			while (file_data):
				file_data = file_part.read(4096)
				final_file.write(file_data)

			file_part.close()
			utils_file_input.size(fileName + '.part' + str(i))
			os.remove(fileName + '.part' + str(i))

		final_file.close()

		md5Comparison = utils_file_input.md5(fileName) == fileMD5
		if not md5Comparison:
			error = 'md5 check failed'
			os.remove(fileName)
		else:
			# offer file
			telnet.offerFile(fileName)

		return md5Comparison, error


def downloadViaTCP(hostIP, size, start, md5, fileName):
	print('//////////////////\n' + 'Downloading from ' + str(hostIP) + '\n//////////////////\n\n')
    
	serverPort = 2030
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((hostIP, serverPort))

	downloadMessage = "DOWNLOAD\n" + md5 + "\n" + str(start) + "\n" + str(size)
	clientSocket.send(downloadMessage.encode())

	receivedFile = open(fileName,'wb')
	dataFromServer = clientSocket.recv(4096)

	status = ''
	if 'DOWNLOAD OK' in dataFromServer:
		response = dataFromServer.split('DOWNLOAD OK\n')
		status = 'DOWNLOAD OK'
	else: 
		response = dataFromServer.split('DOWNLOAD FAILURE\n')
		status = 'DOWNLOAD FAILURE'

	print('pa chequear noma', response)
	global error
	if status == 'DOWNLOAD FAILURE':
		failureType = response[1]
		error = failureType
	elif status == 'DOWNLOAD OK':
		error = ''
		dataFromServer = response[1]
		while (dataFromServer):
			print('==================================RECIBIENDO===================================')
			receivedFile.write(dataFromServer)
			dataFromServer = clientSocket.recv(4096)

	receivedFile.close()
	clientSocket.close()
