################################# PROGRAMA PRINCIPAL #################################
#
# Levantamos todos los hilos que necesitamos que esten corriendo permanentemente
# 

import telnet
import fileSender
import announceSender
import announceListener
from threading import Thread

import signal
import sys

# Inicializamos el thread de Telnet quien recibe los comandos
telnetThread = Thread(target=telnet.telnetServer)
telnetThread.daemon = True
telnetThread.start()

# Inicializamos el thread de fileSender para recibir pedidos de descarga
fileSenderThread = Thread(target=fileSender.startListening)
fileSenderThread.daemon = True
fileSenderThread.start()

# Inicializamos el thread de envio de anuncios
announceSenderThread = Thread(target=announceSender.startSending)
announceSenderThread.daemon = True
announceSenderThread.start()

# Inicializamos el thread que escucha los anuncios
announceListenerThread = Thread(target=announceListener.startListening)
announceListenerThread.daemon = True
announceListenerThread.start()

# Inicializamos el thread para actualizar lista de remote files y borrar los que correspondan
checkAvailabilityThread = Thread(target=announceListener.checkAvailability)
checkAvailabilityThread.deamon = True
checkAvailabilityThread.start()

# manejar cierre forzoso
def signal_handler(sig, frame):
    telnet.forceClose()
    announceListener.forceClose()
    announceSender.forceClose()
    print('Exiting the program now')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.pause()