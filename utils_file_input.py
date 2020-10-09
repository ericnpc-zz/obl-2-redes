
def offeredFiles(files):
    return files.keys()


def displayFile(index, file):
    fileSize = file["size"]
    fileNames = ""
    for name in file["filenames"]:
        fileNames += " "
        fileNames += name

    print str(index) + ". Tamano: " + fileSize + " // Nombres:" + fileNames


def displayFiles(fileList, fileKeys):
    for index, md5 in enumerate(fileKeys, start=1):
        file = fileList[md5]
        displayFile(index, file)


def representedInt(s):
    try: 
        int(s)
        return int(s)
    except ValueError:
        return -1


def captureUserSelection(fileList):
    fileKeys = offeredFiles(fileList)
    displayFiles(fileList, fileKeys)
    md5 = ""

    while True:
        fileIndex = raw_input("\nSeleccione el archivo que desea descargar: ")

        fileIndexInt = representedInt(fileIndex) - 1
        if isinstance(fileIndexInt, int) and fileIndexInt < len(fileKeys) and fileIndexInt >= 0:
            print("\nOK. Se descargara el siguiente archivo:")
            md5 = fileKeys[fileIndexInt]
            file = fileList[md5]
            displayFile(fileIndex, file)
            break
        elif fileIndex == "exit":
            break
        else:
            print("Este archivo no esta disponible. Intente de nuevo.")

    return md5

