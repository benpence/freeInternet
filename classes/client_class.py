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

    def connect(self, protocol, direction, host=protocols._DEFAULT_HOST, port=protocols._DEFAULT_PORT, **kwargs):
        if protocol not in protocols._PROTOCOLS:
            self.log(str(self),
                     "INVALID PROTOCOL. QUITTING"
                     "\n\thost = '%s'"
                     "\n\tport = '%s'" % (host, port),
                     messageType="ERR")
            return False


        # Already connected?
        if self.sock:
            self.sock.close()
            self.sock = None

        self.log(str(self),
                 "Trying to connect..."
                 "\n\thost = '%s'"
                 "\n\tport = '%s'"
                 "\n\tprotocol = '%s'"
                 "\n\tdirection = '%s'" % (host, port, protocol, direction))

        # Connect to server
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))

        #Failed
        except socket.error, (value, message):
            if self.sock:
                self.sock.close()

            self.log(str(self),
                     "Failed to connect"
                     "\n\tmessage = '%s'"
                     "\n\thost = '%s'"
                     "\n\tport = '%s'" % (message, host, port),
                     messageType="ERR")
            return False

        self.log(str(self),
                 "Client connected"
                 "\n\thost = '%s'"
                 "\n\tport = '%s'" % (host, port))

        # Send protocol and direction
        try:
            self.sock.send(protocols.Protocol.pad([protocol, direction]))
        except socket.error, e:
            self.log(str(self),
                     "Failed to send protocol & direction",
                     messageType="ERR")
            

        # Hook for child classes
        actions = protocols._PROTOCOLS[protocol](self, self.sock, direction, socket.gethostname(), **kwargs).actions()
        self.log(str(self),
                 "Running actions")
        while actions.next():
            pass

        self.log(str(self),
                 "Closing connection")

        self.sock.close()
        self.sock = None

        return True

if __name__ == "__main__":
    cli = Client()

    # Test file protocol
    cli.connect("file", protocols.ProtocolFile._JOB_NEW, directory="helper/clientFiles")
    cli.connect("file", protocols.ProtocolFile._JOB_OLD, directory="helper/clientFiles", jobID=123)

    # Test echo protocol
    cli.connect("echo", protocols.ProtocolEcho._FROM_CLIENT)
    cli.connect("echo", protocols.ProtocolEcho._FROM_SERVER)

    # Test message protocol
    notes = ["testing", "testing", "1", "2", "3"]
    cli.connect("message", protocols.ProtocolMessage._FROM_CLIENT, messages=notes)
