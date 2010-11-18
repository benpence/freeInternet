#!/usr/bin/python2.7

import client_class
import socket

class ClientEcho(client_class.Client):
    def __init__(self, **kwargs):
        super(ClientEcho, self).__init__(**kwargs)

    def connectActions(self):
        l = ["hey", "ho", "hiya"]

        for i in l:
            self.sock.send(i)

if __name__ == "__main__":
    cli = ClientEcho()
    cli.connect()
