#!/usr/bin/python2.7

import os #directory paths

import client_class #parent
import protocols

class ClientFile(client_class.Client):
    def __init__(self, directory=protocols._DEFAULT_PATH, **kwargs):
        super(ClientFile, self).__init__(**kwargs)

        self.directory = os.path.join(protocols._ROOT_DIRECTORY, directory)

    def getJobID(self):
        return "123"

    def connectActions(self, sock, direction, address):
        return protocols.ProtocolFile(self, sock, direction, self.directory, address,  jobID=self.getJobID()).actions()


if __name__ == "__main__":
    client = client_class.Client().connect("file", protocols.ProtocolFile._JOB_NEW, directory="helper/clientFiles")
