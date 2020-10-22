import telnet
import fileSender
from threading import Thread

# Inicializamos el thread de Telnet quien recibe los comandos
telnetThread = Thread(target=telnet.telnetServer)
telnetThread.start()

fileSenderThread = Thread(target=fileSender.startListening)
fileSenderThread.start()

# MAIN2
# announceThread = announcesThread(fileList)
# announceThread.start()