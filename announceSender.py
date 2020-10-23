from socket import *
import utils_file_input
import time
import random
import sys
import fileRepository
import threading
from datetime import datetime

SERVER_PORT = 2020
ANNOUNCE_SENDER_LOG_ENABLED = False
MAXIMUM_ANNOUNCE_SIZE = 1450 
# TODO: Agregar fuentes e investigar por que
# TODO: Esperando respuesta de Mati


def getAnnounceMessageList():
	announceMessages = []
	currentAnnounce = []
	previousMessage = ''
	currentMessage = ''

	# dividimos los announces para controlar que pesen menos que el Maximum Announce Size 
	# cuando vemos que no entra ninguno mas, creamos un announce nuevo y damos por finalizado el actual
	for file in fileRepository.getLocalFiles():
		currentAnnounce.append(file)
		currentMessage = utils_file_input.formatAnnounceList(currentAnnounce)
		if sys.getsizeof(currentMessage) > MAXIMUM_ANNOUNCE_SIZE:
			announceMessages.append(previousMessage)
			currentAnnounce = [file]
		previousMessage = currentMessage
	
	announceMessages.append(currentMessage)
	
	if ANNOUNCE_SENDER_LOG_ENABLED:
		print("\n///// ANNOUNCE MESSAGE COUNT IS " + str(len(announceMessages)) + " /////\n")
	return announceMessages



def sendAnnounceMessages(socket):
	if ANNOUNCE_SENDER_LOG_ENABLED:
		print("\n///// START SENDING SCHEDULED ANNOUNCES " + str(datetime.now()) + " /////\n")

	for message in getAnnounceMessageList():
			if ANNOUNCE_SENDER_LOG_ENABLED:
				print("\n///// SENDING ANNOUNCE MESSAGE //////")
				print(message)
			socket.sendto(message.encode(),('<broadcast>', SERVER_PORT))
			time.sleep(random.random())



def startSending(): 
	global clientSocket
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	# https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ
	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
	clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	while True:
		# TODO: Es necesario que este en otro thread?
		threading.Thread(target=sendAnnounceMessages, args=[clientSocket]).start()
		time.sleep(30 + random.random())

	clientSocket.close()

def forceClose():
	global clientSocket
	clientSocket.close()
	print('Announce Sender Socket Closed')