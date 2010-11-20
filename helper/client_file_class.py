#!/usr/bin/python2.7

import client_class #parent
import os #directory paths

import protocols

class ClientFile(client_class.Client):
    def __init__(self, directory=protocols._DEFAULT_PATH, **kwargs):
        super(ClientFile, self).__init__(**kwargs)

        self.directory = os.path.join(protocols._ROOT_DIRECTORY, directory)

    def setMode(self, mode, jobID=None):
        self.mode = mode
        self.jobID = jobID

    def connectActions(self, sock):
        sock.send(protocols.Protocol.pad(["file", self.mode]))

        actions = protocols.ProtocolFile.actions(self, sock, self.mode, self.directory, jobID=self.jobID)

        while actions.next():
            pass

if __name__ == "__main__":
    client = ClientFile(directory="helper/clientFiles")
    client.setMode(protocols.ProtocolFile._JOB_OLD, jobID="123")
    client.connect()
