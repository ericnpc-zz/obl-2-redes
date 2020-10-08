from _thread import *
import threading

class thread(threading.Thread):
    def __init__(self):
        super(thread, self).__init__()
        self.active = True
        print "started"

    def run(self):
        print "running"
        while True:
            if self.active == False:
                print "stopping"
                break

    def stop(self):
        self.active = False


print "\n///////////////////////////////////////////////////////"
print "iniciando"

thread1 = thread()
thread1.start()

thread2 = thread()
thread2.start()

global finalizarThread 
finalizarThread = False
programaPrincipal = True

while programaPrincipal:
        print "Numero de Threads Abiertos: " + str(threading.active_count())
        comando = raw_input("Opcion: ")
        if (comando == "1"):
            if thread1.is_alive():
                thread1.stop()
                print "Saliendo del Thread 1."
        elif (comando == "2"):
            if thread2.is_alive():
                thread2.stop()
                print "Saliendo del Thread 2."
        elif (comando == "exit"):
            thread1.stop()
            thread2.stop()
            programaPrincipal = False
        else:
            print "Comando invalido. Intente de nuevo"

print "\nGracias por usar nuestro servicio."
print "///////////////////////////////////////////////////////\n"

# https://www.youtube.com/watch?v=IEEhzQoKtQU&t=0s
# https://dzone.com/articles/python-thread-part-1 