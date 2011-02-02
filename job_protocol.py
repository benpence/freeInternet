import os

from twisted.protocols import basic
from twisted.python import log

import common

_CHUNK_SIZE = 512

class JobProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.ip = self.transport.getPeer().host
        log.msg("Connection")
        
    def connectionLost(self, reason):
        log.msg("Disconnection")
        
    def rawDataReceived(self, data):
        print "RAW DATA RECEIVED"
        log.msg("[Raw Data] Received %d bytes" % len(data))
        
        self.file.write(data)
        
        if data.endswith("\r\n"):
            print "DONE RECEIVING"
            self.file.close
            self.factory.doneReceiving(self.ip, self.file_path)
            self.transport.loseConnection()
            
    def _sendFile(self):
        """
        None -> None
        
        Sends all the binary data of the file
        """
        
        """CHECK FOR FILE PROBLEMS"""
        
        def _readBytesFromFile():
            while True:
                chunk = self.file.read(_CHUNK_SIZE)

                if chunk:
                    yield chunk
                else:
                    break

        def readFile(file_path):
            print "SENDING FILE"
            self.file = open(file_path, 'rb')

            for chunk in _readBytesFromFile():
                self.transport.write(chunk)
            print "SENT FILE"
            self.transport.write("\r\n")
            
                
            """DID EVERYTHING GO SMOOTHLY?"""

            self.file.close()
            print "CLOSING CONNECTION"
            self.transport.loseConnection()

        
        print "SENDING FILE"
        file_path = self.factory.getFile(self.ip)
        print "GOT FILE TO SEND"
        readFile(file_path)
                
    def _receiveFile(self):
        """
        None -> None
        
        Sets up protocol to receive a file
        """
        
        """CHECK FOR FILE PROBLEMS"""
        
        self.file_path = os.path.join(
            self.factory.file_directory,
            common.random_hash())
        
        self.file = open(self.file_path, 'wb')
        self.setRawMode()

class JobServerProtocol(JobProtocol):
    _ACTIONS = {
        "RECEIVE" : lambda self: self._receiveFile(),
        "SEND"    : lambda self: self._sendFile(),
        }
        
    def lineReceived(self, line):
        """ADD SOME ERROR CHECKING HERE"""
        
        action = line.strip()
        print "'%s'" % action
        
        # Valid commands?                        
        if action not in self._ACTIONS:
            log.msg("[Action] Invalid Action '%s'" % line)
            self.transport.loseConnection()
            return
        
        log.msg("%s" % action)
        
        # Perform desired function
        self._ACTIONS[action](self)

class JobClientProtocol(JobProtocol):
    _ACTIONS = {
        "RECEIVE" : lambda self: self._sendFile(),
        "SEND"    : lambda self: self._receiveFile(),
        }
    
    def connectionMade(self):
        JobProtocol.connectionMade(self)
        self.factory.clientConnectionMade()
        
        action = self.factory.action
        
        if action not in self._ACTIONS:
            log.msg("[Aciton] Invalid Action '%s'" % action)
            self.transport.loseConnection()
            return
        
        # Tell server what to do
        self.sendLine(action)
        
        # Perform required action
        self._ACTIONS[action](self)