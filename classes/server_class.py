import connection_class
import socket
import select
import sys

import protocols

_BACKLOG = 5 # max number of connections; 5 is standard

class Server(connection_class.Connection):
    """
    Server(output= # boolean logging printed to shell?)

        listens on specified interface (IP), port for connections
    """

    def __init__(self, out=True, **kwargs):
        super(Server, self).__init__(output=out)

        # For passing custom parameters to protocols later
        self.parameters = kwargs

        self.childCount = 0

    def __str__(self):
        return "server%03d" % self.id

    def listen(self, host=protocols._DEFAULT_HOST, port=protocols._DEFAULT_PORT):
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
        # Failed
        except socket.error, (value, message): 
            if self.sock:
                self.sock.close()
            self.log(str(self),
                     "Failed to listen"
                     "\n\tmessage = '%s'"
                     "\n\thost = '%s'"
                     "\n\tport = '%s'" % (message, host, port),
                     messageType = "ERR")

            return False

        self.log(str(self),
                 "Listening"
                 "\n\thost = '%s'"
                 "\n\tport = '%s'" % (host, port))


        #Cycle through connections to service connections with data
        socketToConnection = {self.sock : protocols.Protocol(self, self.sock, "", "127.0.0.1")}
        waitForRecv = [self.sock, sys.stdin]
        waitForSend = []

        while self.running and self.sock:
            # Nonblocking way to manage each connection on one process
            readyForRecv, readyForSend, y = select.select(waitForRecv, waitForSend, [])

            for s in readyForRecv + readyForSend:
                # Server has new connection
                if s is self.sock:
                    client, address = self.sock.accept()

                    self.log(str(self),
                             "[%s] " % address[0],
                             "Received new connection"
                             "\n\thost = '%s'"
                             "\n\tport = '%s'" % (host, port))

                    # Determine protocol
                    try:
                        protocol, direction = protocols.Protocol.unpad(client.recv(protocols._CHUNK_SIZE))
                    except socket.error, e:
                        self.log(str(self),
                                 "[%s] "
                                 "Error receiving" % address[0],
                                 messageType = "ERR")
                        self.running = False
                        break

                    self.log(str(self),
                             "\tprotocol = '%s'"
                             "\n\tdirection = '%s'" % (protocol, direction),
                             continuation=True)

                    # Valid protocol?
                    if protocol in protocols._PROTOCOLS:
                        protocol = protocols._PROTOCOLS[protocol]

                        # Create protocol (generator) with customized parameters
                        parameters = protocol._PARAMETERS
                        socketToConnection[client] = protocol(self,
                                                              client,
                                                              direction,
                                                              address[0],
                                                              **dict([(arg, self.parameters[arg]) for arg in parameters if arg in self.parameters])).actions()
                        waitForSend.append(client)

                    # Bad protocol
                    else:
                        self.log(str(self),
                                 "[%s] "
                                 "BAD PROTOCOL" % address[0],
                                 messageType="ERR")

                # Quit on '\n' from standard input
                elif s is sys.stdin:
                    self.running = False
                    break

                # Runs next step in socket; if done, discards it
                else:
                    nextAction = socketToConnection[s].next()
    
                    # Remove from all lists
                    if s in waitForRecv:
                        waitForRecv.remove(s)

                    if s in waitForSend:
                        waitForSend.remove(s)
                    
                    # Add to next correct list
                    if nextAction == protocols._WAIT_FOR_SEND:
                        waitForSend.append(s)

                    elif nextAction == protocols._WAIT_FOR_RECV:
                        waitForSend.append(s)
                        
                    else:
                        self.log(str(self),
                                 "Closing connection")
                                 
                        socketToConnection.pop(s)
                        s.close()

        self.log(str(self),
                 "Closing server")
        self.sock.close()
        self.sock = None

        return True

if __name__ == "__main__":
    server = Server()
    server.listen()
