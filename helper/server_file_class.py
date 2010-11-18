#!/usr/bin/python2.7

from constants import _ROOT_DIRECTORY
import server_class #Parent

import os #Filepath
import sys #Read/write to stdio
import pickle #Serialize objects
import subprocess #Start new processes from server

_DEFAULT_PATH = ""
_JOIN_CHARACTER = "|"

class ServerFile(server_class.Server):
    """
    ServerFile(filepath= # location to put/look for files,
               **kwargs)

        listens on specified interface (IP), port for connections

        transfer protocol client->server header is "A|B|C|" where
            A = "up" (client->server) or "down" (server->client)
            B = size of file to be transfered in bytes
                If B left blank, server sends "B|..." for filesize
            C = name of file to be transfered
            | = field delimiter 
    """
    def __init__(self, filepath=_DEFAULT_PATH, **kwargs):
        super(ServerFile, self).__init__(**kwargs)

        self.filepath = os.path.join(_ROOT_DIRECTORY, filepath)

    def makeJob(self, client, address, waitForRecv, waitForSend):
        print "NOW i'M HERE"
        header = client.recv(self.chunkSize)
        direction, filesize, filename, rest = header.split(_JOIN_CHARACTER)
        
        #Client->Server
        if direction == "up":
            waitForRecv.append(client)
            return ServerFileJob(client, address, filepath=os.path.join(self.filepath, filename), filesize=int(filesize)).recv()

        #Server->Client
        elif direction == "down": 
            waitForSend.append(client)
            return ServerFileJob(client, address, self.filepath).send()

        else:
            pass #LOG AN ERROR HERE


class ServerFileJob(server_class.ServerJob):
    """
    ServerFileJob(client # client socket,
                  address # client address,
                  filepath= # where file can be found/put,
                  filesize= # size of file)
    """

    def __init__(self, client, address, filepath="", filesize=-1, **kwargs):
        super(ServerFileJob, self).__init__(**kwargs)
        self.client = client
        self.address = address
        self.filepath = filepath
        self.filesize = filesize

    def recv(self):
        bytesLeft = self.filesize
        print "filesize = ", self.filesize

        yield True

        file = open(self.filepath, 'wb')

        while bytesLeft > 0:
            if bytesLeft < self.chunkSize:
                file.write(self.client.recv(bytesLeft))
            else:
                file.write(self.client.recv(self.chunkSize))
            bytesLeft -= self.chunkSize

            yield True

        file.close()
        yield False

    def send(self):
        # Tell client the filesize
        filesize = bytesLeft = os.path.getsize(self.filepath)

        yield True

        file = open(self.filepath, 'rb')

        while bytesLeft > 0:
            if bytesLeft < self.chunkSize:
                self.client.send(file.read(bytesLeft))
            else:
                self.client.send(file.read(self.chunkSize))
            bytesLeft -= self.chunkSize

            yield True

        file.close()
        yield False
        
if __name__ == "__main__":
    server = ServerFile(output=True, filepath="helper/serverFiles")
    server.listen()
