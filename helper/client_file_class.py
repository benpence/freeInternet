#!/usr/bin/python2.7

import client_class #parent
import os #directory paths

import constants

class ClientFile(client_class.Client):
    def __init__(self, directory=constants._DEFAULT_PATH, **kwargs):
        super(ClientFile, self).__init__(**kwargs)

        self.directory = os.path.join(constants._ROOT_DIRECTORY, directory)

    def __str__(self):
        return "client%03d" % self.id

    def setMode(self, mode, jobID=None):
        self.mode = mode
        self.jobID = jobID

    def connectActions(self, sock):
        sock.send(constants.Protocol.pad(["file", self.mode]))

        actions = constants.ProtocolFile.actions(self, sock, self.mode, self.directory, jobID=self.jobID)

        while not actions.next():
            pass

if __name__ == "__main__":
    client = ClientFile(directory="helper/clientFiles")
    client.setMode(constants.ProtocolFile._JOB_NEW)
    client.connect()
