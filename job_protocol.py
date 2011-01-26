from twisted.protocols import basic
from twisted.python import log

import common

from job_controller import JobServerController, JobClientController

_CHUNK_SIZE = 512
_SEPARATOR = " "

class JobProtocol(basic.LineReceiver):
    _ACTIONS = {
        "RECEIVE" : _sendFile,
        "SEND"    : _receiveFile,
        }

    def connectionMade(self):
        self.ip = self.transport.getPeer().host
        log.msg("[%s] Connection" % self.ip)
        
    def connectionLost(self, reason):
        log.msg("[%s] Disconnection" % self.ip)
                
    def lineReceived(self, line):
        """ADD SOME ERROR CHECKING HERE"""
        data = self._splitData(line)[0]
        
        if len(data) != 1:
            """ERROR OMG"""
            self.transport.loseConnection()
            return
            
        action = data[0]
        
        if action not in self._ACTIONS:
            log.msg("%s][Action] Invalid Action '%s'" % (self.ip, line))
            self.transport.loseConnection()
            return
        
        log.msg("[%s] %s" % (self.ip, action))
        self._ACTIONS[action]()
        
    def rawDataReceived(self, data):
        log.msg("[%s][Raw Data] Received %d bytes" % (self.ip, len(data)))
        
        self.file.write(data)
        
        if data.endswith("\r\n"):
            d = self.factory.doneReceiving()
            d.addCallBack(self.file.close)
            d.addCallback(self.loseConnection)
            
    def _sendFile(self):
        def _readFile(fil_path):
            self.file = open(file_path, 'rb')

            for chunk in self._readBytesFromFile(self):
                self.transport.write(chunk)
                
            """DID EVERYTHING GO SMOOTHLY?"""

            self.file.close()

        d = self.factory.getFile(self.ip)
        d.addCallback(sendFile)

    def _readBytesFromFile(self):
        while True:
            chunk = self.file.read(_CHUNK_SIZE)

            if chunk:
                yield chunk
            else:
                break
                
    def _receiveFile(self):
        """
        None -> None
        
        Sets up protocol to receive a file
        """
        
        """CHECK FOR FILE PROBLEMS"""
        
        self.file_path = "%s" % common._random_hash()
        
        self.file = open(filename, 'wb')
        self.setRawMode()
            
    @classmethod
    def _splitData(cls, data):

        """SPLIT DATA"""

        return data.strip().split(_SEPARATOR)