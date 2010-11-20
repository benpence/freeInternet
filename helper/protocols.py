import os
import logging

_ROOT_DIRECTORY = "/home/bmp/Source/Free-Internet/"
_DEFAULT_PATH = ""

_DEFAULT_HOST = 'localhost'
_DEFAULT_PORT = 5555
_CHUNK_SIZE = 4096

_JOIN_CHARACTER = "|"
_WAIT_FOR_SEND = "send"
_WAIT_FOR_RECV = "recv"

class ProtocolEcho(object):
    _FROM_CLIENT = "fromClient"
    _FROM_SERVER = "fromServer"

    _WAIT_FOR = _WAIT_FOR_SEND

    @classmethod
    def actions(cls, type, sock, direction, directory):
        if direction == ProtocolEcho._FROM_CLIENT:
            if str(type).startswith("server"):
                return ProtocolEcho.recv(sock)
            else:
                return ProtocolEcho.send(sock)
                
        elif direction == ProtocolEcho._FROM_SERVER:
            if str(type).startswith("server"):
                return ProtocolEcho.send(sock)
            else:
                return ProtocolEcho.recv(sock)

        else:
            logging.Logger.log(str(type),
                               "BAD DIRECTION",
                               messageType = "ERR")
            return Protocol.dummyActions()

    @classmethod
    def send(cls, sock):
        yield "send"
        sock.send(Protocol.pad("GOOD MORNING"))

        yield "recv"
        data = Protocol.unpad(sock.recv(_CHUNK_SIZE))
        print data

        yield "send"
        sock.send(Protocol.pad("HOW ARE YOU?"))

        yield "recv"
        data = Protocol.unpad(sock.recv(_CHUNK_SIZE))
        print data

        yield "send"
        sock.send(Protocol.pad("TA"))

        yield "recv"
        data = Protocol.unpad(sock.recv(_CHUNK_SIZE))
        print data

        yield None

    @classmethod
    def recv(cls, sock):

        yield "recv"
        data = Protocol.unpad(sock.recv(_CHUNK_SIZE))
        print data

        yield "send"
        sock.send(Protocol.pad("GOOD MORNING"))

        yield "recv"
        data = Protocol.unpad(sock.recv(_CHUNK_SIZE))
        print data

        yield "send"
        sock.send(Protocol.pad("GOOD, GOOD."))

        yield "recv"
        data = Protocol.pad(sock.recv(_CHUNK_SIZE))
        print data

        yield "send"
        sock.send(Protocol.pad("TA"))

        yield None

class ProtocolFile(object):
    _JOB_NEW = "new"
    _JOB_OLD = "old"

    _WAIT_FOR = _WAIT_FOR_SEND

    @classmethod
    def actions(cls, type, sock, direction, directory, jobID=None):
        if direction == ProtocolFile._JOB_NEW:
            if str(type).startswith("server"):
                return ProtocolFile.send(sock, directory, ProtocolFile.getJobID())
            else:
                return ProtocolFile.recv(sock, directory)
                
        elif direction == ProtocolFile._JOB_OLD:
            if str(type).startswith("server"):
                return ProtocolFile.recv(sock, directory)
            else:
                return ProtocolFile.send(sock, directory, jobID)

        else:
            logging.Logger.log(str(type),
                               "BAD DIRECTION",
                               messageType = "ERR")
            return Protocol.dummyActions()

    @classmethod
    def getJobID(cls):
        return str(123)

    @classmethod
    def send(cls, sock, directory, jobID):
        yield "send"
        sock.send(Protocol.pad(jobID))

        yield "send"
        filepath = os.path.join(directory, jobID)
        filesize = bytesLeft = os.path.getsize(filepath)

        sock.send(Protocol.pad(str(filesize)))

        file = open(filepath, 'rb')

        while bytesLeft > 0:
            yield "send"
            if bytesLeft < _CHUNK_SIZE:
                sock.send(file.read(bytesLeft))
            else:
                sock.send(file.read(_CHUNK_SIZE))
            bytesLeft -= _CHUNK_SIZE

        file.close()

        yield None

    @classmethod
    def recv(cls, sock, directory):
        yield "recv"
        jobID = Protocol.unpad(sock.recv(_CHUNK_SIZE))


        yield "recv"
        filesize = bytesLeft = int(Protocol.unpad(sock.recv(_CHUNK_SIZE)))

        filepath = os.path.join(directory, jobID)
        file = open(filepath, 'wb')

        while bytesLeft > 0:
            yield "recv"
            if bytesLeft < _CHUNK_SIZE:
                file.write(sock.recv(bytesLeft))
            else:
                file.write(sock.recv(_CHUNK_SIZE))
            bytesLeft -= _CHUNK_SIZE

        file.close()

        yield None

class Protocol(object):
    _PROTOCOLS = {"file" : ProtocolFile,
                  "echo" : ProtocolEcho}

    @classmethod
    def pad(cls, l):
        if type(l) is list:
            string = _JOIN_CHARACTER.join(l) + _JOIN_CHARACTER
        else:
            string = l + _JOIN_CHARACTER

        while len(string) < _CHUNK_SIZE:
            string += "."
        return string

    @classmethod
    def unpad(cls, t):
        l = t.split(_JOIN_CHARACTER)[:-1]
        
        if len(l) == 1:
            return l[0]
        else:
            return l

    @classmethod
    def dummyActions(cls):
        yield False

