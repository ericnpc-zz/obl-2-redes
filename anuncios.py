def announce(localFiles): 
    
    message = "ANNOUNCE\n"
    for file in localFiles
        message =+ "<" + file[fileName] + ">\t<" + str(file[size]) + ">\t<" + file[md5] + ">\n"

    return message