import testing_md5
import anuncios

remoteFiles = []

# localFiles.append({
# 	fileName: 'pepito.js',
# 	fileSize: 203859400,
# 	fileMD5: 'hdaksehqi378437n73qkay3874q3'
# })

# remoteFiles.append({
    # 	hostIPs: ['121.21.21.3', '234.325.123.12'],
    # 	names: ['pepito.js', 'perrito.js'],
    #   size: 234234234
# })


def listRemoteFiles():

    remoteFilesString = ''
    fileId = 0

    # lock remoteFiles
    for file in remoteFiles.values()
    
        fileName = ''
        for fileName in file[names]
            fileNames += fileName ', '

        remoteFilesString =+ f"{fileId + 1}\t{file[size]}\t{fileNames}" 
    # unlock remoteFiles                         

    return remoteFilesString

def updateRemoteFiles():


def offerFile(path): 

    _md5 = testing_md5.md5(path)
    _size = testing_md5.size(path)

    anuncios.localFiles.append({
        "md5": _md5,
        "size": _size,
        "fileName": path
    })

    return anuncios.localFiles
