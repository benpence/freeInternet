import os
import socket
import logging

_ROOT_DIRECTORY = "%s%s" % os.getcwd().partition("FreeInternet")[:2]

_DEFAULT_HOST = 'savannah.cs.gwu.edu'
_DEFAULT_PORT = 5555
_CHUNK_SIZE = 512

_JOIN_CHARACTER = "|"
_PAD_CHARACTER = "."

_WAIT_FOR_SEND = "send"
_WAIT_FOR_RECV = "recv"

class Protocol(object):
    def __init__(self, caller, sock, direction, address):
        self.caller = caller
        self.sock = sock
        self.direction = direction
        self.address = address

    def __str__(self):
        return self.address

    @classmethod
    def pad(cls, l):
        if type(l) is list:
            string = _JOIN_CHARACTER.join(l) + _JOIN_CHARACTER
        else:
            string = l + _JOIN_CHARACTER

        while len(string) < _CHUNK_SIZE:
            string += _PAD_CHARACTER
        return string

    @classmethod
    def unpad(cls, t):
        l = t.split(_JOIN_CHARACTER)[:-1]
        
        if len(l) == 1:
            return l[0]
        else:
            return l

    def writeFile(self, file, data):
        try:
            file.write(data)
        except IOError, e:
            logging.Logger.log(str(self.caller),
                               "[%s] "
                               "Error writing to file %s" % (str(self), file.name),
                               messageType="ERR")
            raise StopIteration()

    def readFile(self, file, amount=_CHUNK_SIZE):
        try:
            data = file.read(amount)
        except IOError, e:
            logging.Logger.log(str(self.caller),
                               "[%s] "
                               "Error reading from file %s" % (str(self), file.name),
                               messageType="ERR")
            raise StopIteration()
        return data


    def sendData(self, data, binary=None):
        try:
            if binary:
                self.sock.send(data)
            else:
                self.sock.send(Protocol.pad(data))
        except socket.error, e:
            logging.Logger.log(str(self.caller),
                               "[%s] "
                               "Error sending" % str(self),
                               messageType = "ERR")
            raise StopIteration()
        return True

    def recvData(self, binary=None):
        try:
            if binary:
                data = self.sock.recv(binary)
            else:
                data = Protocol.unpad(self.sock.recv(_CHUNK_SIZE))
        except socket.error, e:
            logging.Logger.log(str(self.caller),
                               "[%s] "
                               "Error receiving" % str(self),
                               messageType = "ERR")
            raise StopIteration()
        return data

    def actions(self):
        pass
                    
    def dummyActions(self):
        yield None

class ProtocolEcho(Protocol):
    _FROM_CLIENT = "fromClient"
    _FROM_SERVER = "fromServer"

    _PARAMETERS = {}

    def __init__(self, caller, sock, direction, address):
        super(ProtocolEcho, self).__init__(caller, sock, direction, address)

    def actions(self):
        # Client -> Server
        if self.direction == self._FROM_CLIENT:
            # Server
            if "server" in str(self.caller):
                return self.recv()

            # Client
            else:
                return self.send()
                
        # Server -> Client
        elif self.direction == self._FROM_SERVER:
            # Server
            if "server" in str(self.caller):
                return self.send()

            # Client
            else:
                return self.recv()

        else:
            logging.Logger.log(str(self.caller),
                               "[%s] "
                               "BAD DIRECTION" % str(self),
                               messageType = "ERR")
            return self.dummyActions()

    def send(self):
        yield _WAIT_FOR_SEND
        self.sendData("GOOD MORNING")

        yield _WAIT_FOR_RECV
        data = self.recvData()
        print data

        yield _WAIT_FOR_SEND
        self.sendData("HOW ARE YOU?")

        yield _WAIT_FOR_RECV
        data = self.recvData()
        print data

        yield _WAIT_FOR_SEND
        self.sendData("TA")

        yield _WAIT_FOR_RECV
        data = self.recvData()
        print data

        yield None

    def recv(self):
        yield _WAIT_FOR_RECV
        data = self.recvData()
        print data

        yield _WAIT_FOR_SEND
        self.sendData("GOOD MORNING")

        yield _WAIT_FOR_RECV
        data = self.recvData()
        print data

        yield _WAIT_FOR_SEND
        self.sendData("GOOD, GOOD.")

        yield _WAIT_FOR_RECV
        data = self.recvData()
        print data

        yield _WAIT_FOR_SEND
        self.sendData("TA")

        yield None

class ProtocolMessage(ProtocolEcho):
    _FROM_CLIENT = "fromClient"
    _FROM_SERVER = "fromServer"

    _END_OF_STREAM = '\\'

    _PARAMETERS = {}

    def __init__(self, caller, sock, direction, address, messages=[]):
        super(ProtocolMessage, self).__init__(caller, sock, direction, address)
        self.messages = messages

    def send(self):
        for message in self.messages:
            self.sendData(message)
            yield _WAIT_FOR_SEND
        
        yield _WAIT_FOR_SEND
        self.sendData(self._END_OF_STREAM)

        yield None

    def recv(self):

        yield _WAIT_FOR_RECV
        data = self.recvData()

        while data != self._END_OF_STREAM:
            print data
            yield _WAIT_FOR_RECV
            data = self.recvData()

        yield None

class ProtocolFile(Protocol):
    _JOB_NEW = "new"
    _JOB_OLD = "old"

    _PARAMETERS = {"jobDirectory"     : os.path.join(_ROOT_DIRECTORY, "classes", "serverFiles"),
                   "getJobIDFunction" : lambda : 0,
                   "updateDatabase"   : lambda : 0}

    def __init__(self, caller, sock, direction, address, jobDirectory=_PARAMETERS["jobDirectory"], jobID=None, getJobIDFunction=_PARAMETERS["getJobIDFunction"], updateDatabase=None):
        super(ProtocolFile, self).__init__(caller, sock, direction, address)

        self.directory = os.path.join(_ROOT_DIRECTORY, jobDirectory)

        if jobID is not None:
            self.jobID = jobID

        if getJobIDFunction:
            self.getJobIDFunction = getJobIDFunction

        if updateDatabase:
            self.updateDatabase = updateDatabase

    def actions(self):
        # Server -> Client
        if self.direction == self._JOB_NEW:
            # Server
            if "server" in str(self.caller):
                return self.send(self.getJobID())

            # Client
            else:
                return self.recv()
                
        # Client -> Server
        elif self.direction == self._JOB_OLD:
            # Server
            if "server" in str(self.caller):
                return self.recv()

            # Client
            else:
                return self.send(self.jobID)

        else:
            logging.Logger.log(str(self.caller),
                               "[%s] "
                               "BAD DIRECTION" % str(self),
                               messageType = "ERR")
            return self.dummyActions()

    def getJobID(self):
        return self.getJobIDFunction(self.address)

    def send(self, jobID):
        # Send jobID
        yield _WAIT_FOR_SEND
        self.sendData("%06d" % jobID)

        # Send filesize
        yield _WAIT_FOR_SEND
        filepath = os.path.join(self.directory, "%06d.send" % jobID)
        filesize = bytesLeft = os.path.getsize(filepath)
        self.sendData(str(filesize))

        # Send file binary data
        file = open(filepath, 'rb')

        while bytesLeft > 0:
            yield _WAIT_FOR_SEND
            if bytesLeft < _CHUNK_SIZE:
                self.sendData(self.readFile(file, amount=bytesLeft), binary=True)
            else:
                self.sendData(self.readFile(file), binary=True)
            bytesLeft -= _CHUNK_SIZE

        file.close()

        yield None

    def recv(self):
        # Receive jobID
        yield _WAIT_FOR_RECV
        jobID = self.recvData()

        # Receive filesize
        yield _WAIT_FOR_RECV
        filesize = bytesLeft = int(self.recvData())

        # Receive file binary data
        filepath = os.path.join(self.directory, jobID + ".recv")
        file = open(filepath, 'wb')

        while bytesLeft > 0:
            yield _WAIT_FOR_RECV
            if bytesLeft < _CHUNK_SIZE:
                self.writeFile(file, self.recvData(binary=bytesLeft))
            else:
                self.writeFile(file, self.recvData(binary=_CHUNK_SIZE))
            bytesLeft -= _CHUNK_SIZE

        file.close()

        # Run adminisrative tasks if necessary
        if "job_server" in str(self.caller):
            self.updateDatabase(self.address, int(jobID))

        yield None


_PROTOCOLS = {"file"    : ProtocolFile,
              "echo"    : ProtocolEcho,
              "message" : ProtocolMessage}
