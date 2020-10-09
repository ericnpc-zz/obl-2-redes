from utils_file_input import *
from announcesThread import *

# ejemplo de files
dict1 = {
    "size": "34kb",
    "filenames": ["pic.jpg", "wook.png", "cat.svg"]
}

dict2 = {
    "size": "89kb",
    "filenames": ["kat.jpg", "ok.png", "dog.svg"]
}

fileList = {}
fileList["askjdlajda"] = dict1
fileList["4802384092"] = dict2

# inicializo thread con lista
announceThread = announcesThread(fileList)
announceThread.start()

# capturo seleccion del usuario
md5 = captureUserSelection(fileList)

if md5 == "":
    print("\nAborto Exitoso\n")
else:
    print("\nDescargando el archivo con MD5: " + md5)

# actualizando lista de archivos del thread
newFileList = {}
newFileList["TUVIEJA"] = dict1
announceThread.setFileList(newFileList)