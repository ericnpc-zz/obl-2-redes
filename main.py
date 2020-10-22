import telnet
import fileSender
import announceSender
from threading import Thread

# Inicializamos el thread de Telnet quien recibe los comandos
telnetThread = Thread(target=telnet.telnetServer)
telnetThread.start()

fileSenderThread = Thread(target=fileSender.startListening)
fileSenderThread.start()

announceThread = Thread(target=announceSender.startSending)
announceThread.start()