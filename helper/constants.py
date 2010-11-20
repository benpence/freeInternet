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

class ProtocolFile(object):
    _JOB_NEW = "new"
    _JOB_OLD = "old"

    _WAIT_FOR = _WAIT_FOR_RECV # In which queue the server will place these actions

    @classmethod
    def actions(cls, type, sock, direction, directory, jobID=None):
        print direction
        print str(type)
        if direction == ProtocolFile._JOB_NEW:
            print str(type)
            if str(type).startswith("server"):
                print "1"
                return ProtocolFile.send(sock, directory, ProtocolFile.getJobID())
            else:
                print "2"
                return ProtocolFile.recv(sock, directory)
                
        elif direction == ProtocolFile._JOB_OLD:
            print str(type)
            if str(type).startswith("server"):
                print "3"
                return ProtocolFile.recv(sock, directory)
            else:
                print "4"
                return ProtocolFile.send(sock, directory, jobID)

        else:
            print "5"
            logging.Logger.log(str(type),
                               "BAD DIRECTION",
                               messageType = "ERR")
            return Protocol.dummyActions()

    @classmethod
    def getJobID(cls):
        return str(123)

    @classmethod
    def send(cls, sock, directory, jobID):
        sock.send(Protocol.pad([jobID]))

        yield True

        filepath = os.path.join(directory, jobID)
        filesize = bytesLeft = os.path.getsize(filepath)

        sock.send(Protocol.pad([str(filesize)]))

        yield True

        file = open(filepath, 'rb')

        while bytesLeft > 0:
            if bytesLeft < _CHUNK_SIZE:
                sock.send(file.read(bytesLeft))
            else:
                sock.send(file.read(_CHUNK_SIZE))
            bytesLeft -= _CHUNK_SIZE

            yield True

        file.close()

        yield False

    @classmethod
    def recv(cls, sock, directory):
        jobID = Protocol.unpad(sock.recv(_CHUNK_SIZE))[0]

        print "DOING MY THENG"

        yield True

        print "DOING MY THUNG"

        filesize = bytesLeft = int(Protocol.unpad(sock.recv(_CHUNK_SIZE))[0])

        print "DOING MY THANG"

        yield True

        filepath = os.path.join(directory, jobID)
        file = open(filepath, 'wb')

        print "DOING MY THING"

        while bytesLeft > 0:
            if bytesLeft < _CHUNK_SIZE:
                file.write(sock.recv(bytesLeft))
            else:
                file.write(sock.recv(_CHUNK_SIZE))
            bytesLeft -= _CHUNK_SIZE
            yield True

        file.close()

        yield False

class Protocol(object):
    _PROTOCOLS = {"file" : ProtocolFile}

    @classmethod
    def pad(cls, l):
        string = _JOIN_CHARACTER.join(l) + _JOIN_CHARACTER

        while len(string) < _CHUNK_SIZE:
            string += "."
        return string

    @classmethod
    def unpad(cls, t):
        return t.split(_JOIN_CHARACTER)[:-1]

    @classmethod
    def dummyActions(cls):
        yield False

