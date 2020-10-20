import testing_md5
from threading import Thread, Lock

# import telnetThread
# import anuncios

remoteFiles = {}
localFiles = []

localFiles.append({
	'fileName': 'pepito.js',
	'size': 203859400,
	'md5': 'hdaksehqi378437n73qkay3874q3'
})

remoteFiles['hdaksehqi378437n73qkay3874q']= {
        'size': 115
        'hosts': [ {'ip': '192.168.1.5',
                    'name': '/Users/nadiarecarey/Desktop/Screen Recording 2020-10-14 at 7.21.45 PM.mov'
                    'lastAnnounced': datetime.now()
                    }, 
                    {'ip': '234.325.123.12',
                     'name': 'perrito.js',
                     'lastAnnounced': datetime.now()
                    }
                  ]        
}

# getter de remoteFiles, solo se va a acceder a esta var
# global, llamando a esta funcion
def getRemoteFiles():
    mutex = Lock()
    mutex.acquire()
    _remoteFiles = remoteFiles.copy()
    mutex.release()
    return _remoteFiles

# setter de remoteFiles, solo se va a acceder a esta var
# global, llamando a esta funcion
def setRemoteFiles():
    print('conchudo')
    # mutex = Lock()
    # mutex.acquire()
    # _remoteFiles = remoteFiles.copy()
    # mutex.release()
    # return _remoteFiles


def listRemoteFiles():

    remoteFilesString = ''
    fileId = 0

    # lock remotseFiles 
    for key in list(remoteFiles.keys()):
        print(key)
        f = remoteFiles[key]
        print(f)
        fileName = ''
        for fileName in f.items():
            fileNames += fileName + ', '

        remoteFilesString =+ "{fileId + 1}\t{file[size]}\t{fileNames}\n"
    # unlock remoteFiles

    return remoteFilesString

# def updateRemoteFiles():


def offerFile(path):

    _md5 = testing_md5.md5(path)
    _size = testing_md5.size(path)

    localFiles.append({
        "md5": _md5,
        "size": _size,
        "fileName": path
    })

    return localFiles

def getFile(fileMD5):
    file = file

# telnetCliThread = telnetThread()
# telnetCliThread.start()


# MAIN2
# # inicializo thread con lista
# announceThread = announcesThread(fileList)
# announceThread.start()

# # capturo seleccion del usuario
# md5 = captureUserSelection(fileList)

# if md5 == "":
#     print("\nAborto Exitoso\n")
# else:
#     print("\nDescargando el archivo con MD5: " + md5)

# # actualizando lista de archivos del thread
# newFileList = {}
# newFileList["TUVIEJA"] = dict1
# announceThread.setFileList(newFileList)