from _thread import *
import threading
import random
import time

class announcesThread(threading.Thread):

    def __init__(self, fileList):
        super(announcesThread, self).__init__()
        self.active = True
        self.fileList = fileList

    def run(self):
        while True:
            time.sleep(5 + random.random()) # TODO: Tiene que ser 30 segs
            print "\nTime to announce!"
            print self.fileList
            print "\n"

            if self.active == False:
                break

    def stop(self):
        self.active = False

    def setFileList(self, newFileList):
        self.fileList = newFileList

        print "\nSet new file list"
        print self.fileList
        print "\n"
