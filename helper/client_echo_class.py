#!/usr/bin/python

import client_class #parent
import os #directory paths

import protocols

class ClientEcho(client_class.Client):
    def __init__(self, **kwargs):
        super(ClientEcho, self).__init__(**kwargs)

    def setMode(self, mode):
        self.mode = mode

    def connectActions(self, sock):
        sock.send(protocols.Protocol.pad(["echo", self.mode]))

        actions = protocols.ProtocolEcho.actions(self, sock, self.mode, "")

        while actions.next():
            pass

if __name__ == "__main__":
    client = ClientEcho()
    client.setMode(protocols.ProtocolEcho._FROM_SERVER)
    client.connect()
