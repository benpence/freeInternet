#!/usr/bin/python2.7

import client_class #parent
import os #directory paths

from constants import _ROOT_DIRECTORY

_DEFAULT_PATH = ""
_JOIN_CHARACTER = "|"

class ClientFile(client_class.Client):
    def __init__(self, filepath=_DEFAULT_PATH, **kwargs):
        super(ClientFile, self).__init__(**kwargs)

        self.filepath = os.path.join(_ROOT_DIRECTORY, filepath)

    def setFile(self, direction, filename):
        self.direction = direction
        self.filename = filename

    def connectActions(self):
        # Client->Server
        self.filepath = os.path.join(self.filepath, self.filename)

        # Nonexistent file?
        if not os.path.exists(self.filepath):
            self.log("client%03d" % self.id,
                     "file to send not found"
                     "\n\tdirection = '%s'"
                     "\n\tsource = '%s'" % (self.direction, self.filepath),
                     messageType="ERR")
            return False

        filesize = bytesLeft = os.path.getsize(self.filepath)

        # Send header
        header = _JOIN_CHARACTER.join([self.direction,
                                       str(os.path.getsize(self.filepath)),
                                       self.filename,
                                       ""])
        self.sock.send(self.pad(header))

        # Transfer pieces to server
        file = open(self.filepath, 'rb')
        while bytesLeft > 0:
            if bytesLeft < self.chunkSize:
                self.sock.send(file.read(bytesLeft))
            else:
                self.sock.send(file.read(self.chunkSize))
            bytesLeft -= self.chunkSize

        '''self.log("client%03d" % self.id,
                 "sent %d bytes of '%s' to server" % (filesize, self.filepath))

        # Server->Client
        elif direction == "down":
            destination = os.path.join(self.filepath, filename)

            # Send header
            header = _JOIN_CHARACTER.join([    direction,
                                            "",
                                            filename,
                                            ""])
            self.sock.send(self.pad(header))

            # Receive filesize
            data = self.sock.recv(self.chunkSize)
            filesize = bytesLeft = int(data.split(_JOIN_CHARACTER)[0])

            # Receive file chunks
            with open(destination, 'wb') as file:
                while bytesLeft > 0:
                    if bytesLeft < self.chunkSize:
                        file.write(self.sock.recv(bytesLeft))
                    else:
                        file.write(self.sock.recv(self.chunkSize))
                    bytesLeft -= self.chunkSize

            self.log(    "client%03d" % self.id,
                        "received %d into file '%s'" % (filesize, destination))
        else:
            self.log(    "client%03d" % self.id,
                        "bad protocol"
                        "\n\tdirection = '%s'"
                        "\n\tfilename = '%s'" % (direction, filename),
                        messageType = "ERR")

            return False

        header = _JOIN_CHARACTER.join(["done", "", "", ""])
        self.sock.send(self.pad(header))

        self.fileQueue = []

        return True
            '''

if __name__ == "__main__":
    client = ClientFile(output=True, filepath="helper/clientFiles")
    client.setFile("up", "test")
    client.connect()
