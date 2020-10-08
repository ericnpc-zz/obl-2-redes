import os
from testing_md5 import md5

# logica de offer
listaOfrecidos = []

def fileinfo(fname):
    f = open(fname, "r")
    size = os.stat(fname).st_size 
    mdfive = md5(fname)
    f.close()
    return "<" + fname + ">\\t<" + str(size) + ">\\t<" + mdfive + ">\\n"

# todo: pasar el archivo a bytes

while True:
        comando = raw_input("\nComandos disponibles: offer <filename>\n")

        if (comando[0:6] == "offer "):
            listaOfrecidos.append(fileinfo(comando[6:]))
        else:
            print "Comando no valido"

        print "\n"
        print "ANNOUNCE\\n"
        for elem in listaOfrecidos:
            print elem
