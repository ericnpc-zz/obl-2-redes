
# Documentacion sobre manejo de memoria en python:

# Las variables globales tienen scope en el modulo (mismo file)
# https://stackoverflow.com/questions/13881395/in-python-what-is-a-global-statement
# https://www.tutorialspoint.com/Explain-the-visibility-of-global-variables-in-imported-modules-in-Python

# Modules are singletons in Python because import only creates a single copy of each module
# https://python-patterns.guide/gang-of-four/singleton/

# La responsabilidad de este modulo es mantener las estructuras globales de archivos 
# locales y remotos.

from threading import Thread, Lock
from datetime import datetime

remoteFiles = {}
localFiles = []

# Ejemplo de LocalFiles:
# localFiles = [
# {
#     'fileName': 'File1.ext',
#     'size': 34252343,
#     'md5': 'MD5file1'
# },
# {
#     'fileName': 'File2.ext',
#     'size': 55867633,
#     'md5': 'MD5file2'
# }
# ]

# Ejemplo de remoteFiles
# remoteFiles = {
#   'md5file1': 
#      {
#         'size': 38173178,
#         'hosts': [ {'ip': '192.168.1.23',
#                     'name': 'fileOfrecidoPorHost1.txt',
#                     'lastAnnounced': lastTimeAnnounced
#                     }, 
#                     {'ip': '10.0.1.133',
#                      'name': 'fileOfrecidoPorHost2.ext',
#                      'lastAnnounced': lastTimeAnnounced
#                     }
#                   ]   
#       }  
# }

localFileLock = Lock()
remoteFileLock = Lock()

def getLocalFiles():
    localFileLock.acquire()
    global localFiles
    _localFiles = localFiles[:]
    localFileLock.release()
    return _localFiles

def setLocalFile(localFile):
    localFileLock.acquire()
    global localFiles
    localFiles.append(localFile)
    localFileLock.release()

def getRemoteFile(md5):
    remoteFileLock.acquire()
    global remoteFiles
    if remoteFiles.has_key(md5):
        _remoteFile = remoteFiles[md5].copy()
    else:
        _remoteFile = {}
    remoteFileLock.release()
    return _remoteFile

def getRemoteFiles():
    remoteFileLock.acquire()
    global remoteFiles
    _remoteFiles = remoteFiles.copy()
    remoteFileLock.release()

    return _remoteFiles

def setRemoteFiles(value):
    remoteFileLock.acquire()
    global remoteFiles
    remoteFiles = value.copy()
    remoteFileLock.release()
