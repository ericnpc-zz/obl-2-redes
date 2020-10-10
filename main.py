import testing_md5
# import telnetThread
# import anuncios

remoteFiles = {}
localFiles = []

localFiles.append({
	'fileName': 'pepito.js',
	'size': 203859400,
	'md5': 'hdaksehqi378437n73qkay3874q3'
})

# TODO: cambiar esta estructura
remoteFiles['hdaksehqi378437n73qkay3874q'] = {
        'hostIPs': ['121.21.21.3', '234.325.123.12'],
        'names': ['pepito.js', 'perrito.js'],
        'size': 234234234
}

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

# telnetCliThread = telnetThread()
# telnetCliThread.start()