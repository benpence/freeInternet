#!/usr/bin/python

import connection_class
import socket
import select

_BACKLOG = 5 # max number of connections; 5 is standard
_DEFAULT_HOST = ''
_DEFAULT_PORT = 5555

class Server(connection_class.Connection):
    """
    Server(chunkSize= # size of data that connection will receive,
           output= # boolean, logging printed to shell?)

        listens on specified interface (IP), port for connections
        passes successful connections to ServerThread threads
    """


    def __init__(self, **kwargs):
        super(Server, self).__init__(**kwargs)

        self.childCount = 0

    def listen(self, host=_DEFAULT_HOST, port=_DEFAULT_PORT):
        """
        listen(host= # IP or domain name to listen on,
               port= # port to listen on)

            start listening for connections
            pass off connection to createThread()
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
            self.log("server%03d" % self.id,
                     "socket failed to listen"
                     "\n\tmessage = '%s'"
                     "\n\thost = '%s'"
                     "\n\tport = '%s'" % (message, host, port),
                     messageType = "ERR")

            return False

        self.log("server%03d" % self.id,
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
                # Server has new connection
                if s is self.sock:
                    client, address = self.sock.accept()

                    self.log("server%03d" % self.id,
                             "Creating server child"
                             "\n\thost = '%s'"
                             "\n\tport = '%s''" % (host, port))

                    # Hook for child classes
                    socketToConnection[client] = self.makeJob(client, address, waitForRecv, waitForSend)

                # Runs next step in socket; if done, discards it
                elif not socketToConnection[s].next():
                    socketToConnection.pop(s)
                    s.close()

        self.sock.close()
        self.sock = None

        return True

    def makeJob(self, client, address, waitForRecv, waitForSend):
        """
        makeJob(client # the client socket,
                address # the address of the cilent,
                waitForRecv # append to this list for client->server
                waitForSend # append to this list for server->client)
        """
        pass

if __name__ == "__main__":
    server = Server()
    server.listen()
