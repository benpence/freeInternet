#!/usr/bin/python

import server_class
import socket

class ServerEcho(server_class.Server):
    def __init__(self, **kwargs):
        super(ServerEcho, self).__init__(**kwargs)

    def makeJob(self, client, address, waitForRecv, waitForSend):
        waitForRecv.append(client)
        return ServerEchoJob(client, address).tasks()

class ServerEchoJob:
    def __init__(self, client, address):
        self.client = client
        self.address = address

    def tasks(self):
        data = self.client.recv(4096)

        while data:
            print data
            yield True
            data = self.client.recv(4096)

        yield False

if __name__ == "__main__":
    server = ServerEcho()
    server.listen()
