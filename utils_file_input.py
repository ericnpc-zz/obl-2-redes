
def offeredFiles(files):
    return files.keys()


def getFileDescription(index, file):
    fileSize = file["size"]
    fileNames = ""
    for name in file["names"]:
        fileNames += " "
        fileNames += name + ', '

    return str(index) + ". Tamano: " + str(fileSize) + " // Nombres:" + fileNames[:-1] + "\n"


def representedInt(s):
    try: 
        int(s)
        return int(s)
    except ValueError:
        return -1


def getFileListDescription(fileList):
    fileKeys = offeredFiles(fileList)
    fileString = ""

    for index, md5 in enumerate(fileKeys, start=1):
        file = fileList[md5]
        fileString += getFileDescription(index, file)
    
    return fileString


def printFileListDescription(fileList):
    print(getFileListDescription(fileList))


def captureUserSelection(fileList):
    fileKeys = offeredFiles(fileList)
    printFileListDescription(fileList)
    md5 = ""

    while True:
        fileIndex = raw_input("\nSeleccione el archivo que desea descargar: ")

        fileIndexInt = representedInt(fileIndex) - 1
        if isinstance(fileIndexInt, int) and fileIndexInt < len(fileKeys) and fileIndexInt >= 0:
            print("\nOK. Se descargara el siguiente archivo:")
            md5 = fileKeys[fileIndexInt]
            file = fileList[md5]
            print(getFileDescription(fileIndex, file))
            break
        elif fileIndex == "exit":
            break
        else:
            print("Este archivo no esta disponible. Intente de nuevo.")

    return md5

def announce(localFiles): 
    message = "ANNOUNCE\n"
    for file in localFiles:
        message += file['fileName'] + "\t" + str(file['size']) + "\t" + file['md5'] + "\n"

    return message
