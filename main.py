import telnet
import fileSender
import announceSender
import announceListener
from threading import Thread

# Inicializamos el thread de Telnet quien recibe los comandos
telnetThread = Thread(target=telnet.telnetServer)
telnetThread.start()

fileSenderThread = Thread(target=fileSender.startListening)
fileSenderThread.start()

announceSenderThread = Thread(target=announceSender.startSending)
announceSenderThread.start()

announceListenerThread = Thread(target=announceListener.startListening)
announceListenerThread.start()