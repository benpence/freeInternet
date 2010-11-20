#!/usr/bin/python

import connection_class
import socket

import protocols

class Client(connection_class.Connection):
    """
    Client(output= # logging printed to shell?)
    """

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)

    def __str__(self):
        return "client%03d" % self.id

    def connect(self, host=protocols._DEFAULT_HOST, port=protocols._DEFAULT_PORT):
        """
        Set up connection to server
            False     -> Connection failed
            True     -> Connection succeeded
        """

        # Already connected?
        if self.sock:
            self.sock.close()
            self.sock = None

        # Connect to server
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))

        except socket.error, (value, message): #Failed
            if self.sock:
                self.sock.close()

            self.log(str(self),
                     "failed to connect"
                     "\n\tmessage = '%s'"
                     "\n\thost = '%s'"
                     "\n\tport = '%s'" % (message, host, port),
                     messageType="ERR")
            return False

        self.log(str(self),
                 "socket connected"
                 "\n\thost = '%s'"
                 "\n\tport = '%s'" % (host, port))

        # Hook for child classes
        self.connectActions(self.sock)

        self.sock.close()
        self.sock = None

        return True

    def connectActions(self):
        pass

if __name__ == "__main__":
    cli = Client()
    cli.connect()
