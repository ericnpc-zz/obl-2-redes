
# Documentacion sobre manejo de memoria en python:

# Las variables globales tienen scope en el modulo (mismo file)
# https://stackoverflow.com/questions/13881395/in-python-what-is-a-global-statement
# https://www.tutorialspoint.com/Explain-the-visibility-of-global-variables-in-imported-modules-in-Python

# Modules are singletons in Python because import only creates a single copy of each module
# https://python-patterns.guide/gang-of-four/singleton/

from threading import Thread, Lock
from datetime import datetime

remoteFiles = {}
localFiles = []

# Ejemplo de LocalFiles:
# localFiles.append({
# 	'fileName': 'Nombre.ext',
# 	'size': 1234,
# 	'md5': 'MD5'
# })

# remoteFiles[
# 'hdaksehqi378437n73qkay3874q']= {
#         'size': 38173178,
#         'hosts': [ {'ip': 'localhost',
#                     'name': 'archivo_descargado.txt',
#                     'lastAnnounced': datetime.now()
#                     # }, 
#                     # {'ip': '10.0.1.133',
#                     #   'name': 'perrito.ext',
#                     #  'lastAnnounced': datetime.now()
#                     }
                #   ]        
# }

localFileLock = Lock()
remoteFileLock = Lock()

def getLocalFile(index):
    localFileLock.acquire()
    _localFile = localFiles[index].copy()
    localFileLock.release()
    return _localFile

def getLocalFiles():
    localFileLock.acquire()
    _localFiles = localFiles[:]
    localFileLock.release()
    return _localFiles

def setLocalFile(localFile):
    localFileLock.acquire()
    localFiles.append(localFile)
    localFileLock.release()

def getRemoteFile(md5):
    remoteFileLock.acquire()
    _remoteFile = remoteFiles[md5].copy()
    remoteFileLock.release()
    return _remoteFile

def getRemoteFiles():
    remoteFileLock.acquire()
    _remoteFiles = remoteFiles.copy()
    remoteFileLock.release()
    print('=================================> remoteFiles EN GET: ', _remoteFiles)

    return _remoteFiles

def setRemoteFiles(value):
    remoteFileLock.acquire()
    print('======================> value: ', value)
    remoteFiles = value.copy()
    print('======================> remoteFiles: ', remoteFiles)
    remoteFileLock.release()

def deleteRemoteFile(md5):
    remoteFileLock.acquire()
    remoteFiles.pop(md5)
    remoteFileLock.release()