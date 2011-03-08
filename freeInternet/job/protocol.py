import os

from twisted.protocols import basic
from twisted.python import log

import freeInternet.common as common

class JobProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.ip = self.transport.getPeer().host
        log.msg("Connection")
        
    def connectionLost(self, reason):
        log.msg("Disconnection")
        
    def rawDataReceived(self, data):
        if data.endswith("\r\n"):
            data = data[:-2]
            self.file.write(data)
            self.file.close()
            self.factory.doneReceiving(self.ip, self.file_path)
            self.transport.loseConnection()
        else:
            self.file.write(data)
        
            
    def _sendFile(self):
        """
        None -> None
        
        Sends all the binary data of the file
        """
        def _readBytesFromFile():
            while True:
                chunk = self.file.read(common._CHUNK_SIZE)

                if chunk:
                    yield chunk
                else:
                    break

        def readFile(file_path):
            self.setRawMode()
            
            try:
                self.file = open(file_path, 'rb')
                
                for chunk in _readBytesFromFile():
                    self.transport.write(chunk)
                self.transport.write("\r\n")
            except IOError, e:
                print e
            finally:
                if self.file:
                    self.file.close()
                    
                self.transport.loseConnection()
        
        file_path = self.factory.getFile(self.ip)
        readFile(file_path)
                
    def _receiveFile(self):
        """
        None -> None
        
        Sets up protocol to receive a file
        """
        
        self.file_path = os.path.join(
            self.factory.file_directory,
            common.randomHash())
        
        self.file = open(self.file_path, 'wb')
        self.setRawMode()

class JobServerProtocol(JobProtocol):
    _ACTIONS = {
        "RECEIVE" : lambda self: self._receiveFile(),
        "SEND"    : lambda self: self._sendFile(),
        }
        
    def lineReceived(self, line):
        action = line.strip()
        
        # Valid commands?                        
        if action not in self._ACTIONS:
            log.msg("[Action] Invalid Action '%s'" % line)
            self.transport.loseConnection()
            return
    
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
