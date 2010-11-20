#!/usr/bin/python

import connection_class
import socket
import select
import os

import constants

_BACKLOG = 5 # max number of connections; 5 is standard

class Server(connection_class.Connection):
    """
    Server(chunkSize= # size of data that connection will receive,
           output= # boolean, logging printed to shell?)

        listens on specified interface (IP), port for connections
        passes successful connections to ServerThread threads
    """

    def __init__(self, directory=constants._DEFAULT_PATH, **kwargs):
        super(Server, self).__init__(**kwargs)

        self.directory = os.path.join(constants._ROOT_DIRECTORY, directory)
        self.childCount = 0

    def __str__(self):
        return "server%03d" % self.id

    def listen(self, host=constants._DEFAULT_HOST, port=constants._DEFAULT_PORT):
        """
        listen(host= # IP or domain name to listen on,
               port= # port to listen on)

            start listening for connections
            pass off connection to jobs()
        """

        # Already listening
        if self.sock:
            self.sock.close()
            self.sock = None

        # Bind to 'host' on 'port'
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((host, port))
            self.sock.listen(_BACKLOG)

        except socket.error, (value, message): #Failed
            if self.sock:
                self.sock.close()
            self.log(str(self),
                     "socket failed to listen"
                     "\n\tmessage = '%s'"
                     "\n\thost = '%s'"
                     "\n\tport = '%s'" % (message, host, port),
                     messageType = "ERR")

            return False

        self.log(str(self),
                 "socket created"
                 "\n\thost = '%s'"
                 "\n\tport = '%s'" % (host, port))


        #Cycle through connections to service connections with data
        socketToConnection = {self.sock : self}
        waitForRecv = [self.sock]
        waitForSend = []

        while self.running and self.sock:
            # Nonblocking way to manage each connection on one process
            readyForRecv, readyForSend, y = select.select(waitForRecv, waitForSend, [])

            for s in readyForRecv + readyForSend:
                print "GOING THROUGH LOOOOOOOOP"
                # Server has new connection
                if s is self.sock:
                    client, address = self.sock.accept()

                    self.log(str(self),
                             "Received new connection"
                             "\n\thost = '%s'"
                             "\n\tport = '%s'" % (host, port))

                    # Determine protocol
                    print "GETTING PROTOCOL FROM PACKET"
                    protocol, direction = constants.Protocol.unpad(client.recv(self.chunkSize))
                    print "GOT PROTOCOL FROM PACKET"

                    self.log(str(self),
                             "\tprotocol = '%s'"
                             "\n\tdirection = '%s'" % (protocol, direction),
                             continuation=True)

                    print "CHECKING PROTOCOL"
                    if protocol in constants.Protocol._PROTOCOLS:
                        protocol = constants.Protocol._PROTOCOLS[protocol]

                        print "PICKING QUEUE"
                        queue = None

                        if protocol._WAIT_FOR is constants._WAIT_FOR_SEND:
                            queue = waitForRecv
                        else:
                            queue = waitForSend

                        print "BEFORE ACTIONS"
                        actions = socketToConnection[client] = protocol.actions(self, client, direction, self.directory)
                        print "PAST ACTIONS"

                        waitForSend.append(client)
                        #queue.append(client)
                        self.log(str(self),
                                 "\tqueue = %s" % protocol._WAIT_FOR,
                                 continuation=True)

                    # Bad protocol
                    else:
                        self.log(str(self),
                                 "BAD PROTOCOL",
                                 messageType="ERR")

                # Runs next step in socket; if done, discards it
                elif not socketToConnection[s].next():
                    if s in waitForRecv:
                        waitForRecv.remove(s)

                    if s in waitForSend:
                        waitForSend.remove(s)

                    socketToConnection.pop(s)
                    s.close()

        self.sock.close()
        self.sock = None

        return True

if __name__ == "__main__":
    server = Server(directory="helper/serverFiles")
    server.listen()
