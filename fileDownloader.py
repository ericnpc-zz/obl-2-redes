from socket import *
from threading import Thread
import utils
import os
import telnet

global error
error = ''

# Procesa la solicitud de descarga del archivo, a partir de la metadata del mismo. 
# Decide la distribucion de descarga entre los hosts (si mas de uno lo esta ofreciendo)
# abriendo un thread para realizar la descarga desde cada uno. 
# Guardamos cada parte del archivo en disco, para luego de finalizada cada descarga juntar
# las partes en el archivo final. 
# Las partes del archivo son eliminadas del disco luego de finalizada la transaccion.
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

		t = Thread(target=downloadFromSingleHost, args=[host['ip'], size, start, fileMD5, fileName + '.part' + str(i)])
		t.start()
		threads.append(t)
	
	for thread in threads:
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
			utils.size(fileName + '.part' + str(i))
			os.remove(fileName + '.part' + str(i))

		final_file.close()

		md5Comparison = utils.md5(fileName) == fileMD5
		if not md5Comparison:
			error = 'md5 check failed'
			os.remove(fileName)
		else:
			# offer file
			telnet.offerFile(fileName)

		return md5Comparison, error

# Se encarga de establecer la conexion TCP con el host indicado
# para realizar la descarga del archivo solicitado
def downloadFromSingleHost(hostIP, size, start, md5, fileName):
	print('[fileDownloader.downloadFromSingleHost] Downloading from Host: ' + str(hostIP) + '\n')

	serverPort = 2020
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((hostIP, serverPort))

	downloadMessage = "DOWNLOAD\n" + md5 + "\n" + str(start) + "\n" + str(size)
	clientSocket.send(downloadMessage.encode())

	dataFromServer = clientSocket.recv(4096)

	status = ''
	if 'DOWNLOAD OK' in dataFromServer:
		response = dataFromServer.split('DOWNLOAD OK\n')
		status = 'DOWNLOAD OK'
	else: 
		response = dataFromServer.split('DOWNLOAD FAILURE\n')
		status = 'DOWNLOAD FAILURE'

	print('[fileDownloader.downloadFromSingleHost] Download status: ', status + '\n')
	global error
	if status == 'DOWNLOAD FAILURE':
		failureType = response[1]
		error = failureType
	elif status == 'DOWNLOAD OK':
		receivedFile = open(fileName,'wb')
		error = ''
		
		dataFromServer = response[1]
		while (dataFromServer):
			receivedFile.write(dataFromServer)
			dataFromServer = clientSocket.recv(4096)
		
		receivedFile.close()

	print('[fileDownloader.downloadFromSingleHost] Finished downloading from host: ' + str(hostIP) + '. Joining thread\n')

	clientSocket.close()
