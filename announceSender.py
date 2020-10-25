from socket import *
from datetime import datetime
import utils
import time
import random
import sys
import fileRepository
import threading

SERVER_PORT = 2020
MAXIMUM_ANNOUNCE_SIZE = 1450


# Genera uno o mas mensajes de ANNOUNCE (dependiendo del tamano del mensaje) utilizando la lista
# de local files que el host ofrece
def getAnnounceMessageList():
	announceMessages = []
	currentFileList = []
	previousMessage = ''
	currentMessage = ''

	# dividimos los announces para controlar que pesen menos que el Maximum Announce Size 
	# cuando vemos que no entra ninguno mas, creamos un announce nuevo y damos por finalizado el actual
	for file in fileRepository.getLocalFiles():
		currentFileList.append(file)
		currentMessage = utils.formatAnnounceList(currentFileList)

		if sys.getsizeof(currentMessage) > MAXIMUM_ANNOUNCE_SIZE:
			announceMessages.append(previousMessage)
			currentFileList = [file]

		previousMessage = currentMessage
	
	if currentMessage != '':
		announceMessages.append(currentMessage)
	
	print("[announceSender.getAnnounceMessageList] ANNOUNCE MESSAGE COUNT IS " + str(len(announceMessages)) + "\n")
	
	return announceMessages

# Se encarga de enviar los ANNOUNCE tanto en broadcast como unicast
# Si ip = '' mandamos en broadcast, si no, mandamos a ese ip
def sendAnnounceMessages(socket, ip=''):

	print("[announceSender.sendAnnounceMessages] Start sending scheduled announces " + str(datetime.now()) + "\n")

	for message in getAnnounceMessageList():
		# Si el announce es unicast
		if ip != '':
			# espera aleatoria de hasta 5 segundos
			time.sleep(random.uniform(0, 5))
			socket.sendto(message.encode(),(ip, SERVER_PORT))
		else:
			socket.sendto(message.encode(),('<broadcast>', SERVER_PORT))
			time.sleep(random.uniform(0.5, 1))

# Esta funcion va a ser llamada desde un thread que se inicia junto con el programa
# principal. Envia permanentemente (cada 30 segundos mas un tiempo aleatorio) 
# mensajes de tipo ANNOUNCE y REQUEST.
def startSending(): 
	global clientSocket
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	# https://man7.org/linux/man-pages/man7/socket.7.html
	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
	clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	#SEND REQUEST MESSAGE TO DISCOVER REMOTE FILES
	message = "REQUEST\n"
	clientSocket.sendto(message.encode(),('<broadcast>', SERVER_PORT))

	while True:
		if len(fileRepository.getLocalFiles()) > 0:
			threading.Thread(target=sendAnnounceMessages, args=[clientSocket]).start()
		time.sleep(30 + random.uniform(0, 1))


def forceClose():
	global clientSocket
	clientSocket.close()
	print('[announceSender.forceClose] Announce Sender Socket Closed')