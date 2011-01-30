from twisted.protocols import basic
from twisted.python import log

import common

_CHUNK_SIZE = 512
_SEPARATOR = " "

class JobProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.ip = self.transport.getPeer().host
        log.msg("Connection")
        
    def connectionLost(self, reason):
        log.msg("Disconnection")
                
    def lineReceived(self, line):
        """ADD SOME ERROR CHECKING HERE"""
        
        action = self._splitData(line)
        print "'%s'" % action
        
        #if not len(data):
            #"""ERROR OMG"""
            #print "INVALID LENGTH"
            #self.transport.loseConnection()
            #return
                        
        if action not in self._ACTIONS:
            log.msg("[Action] Invalid Action '%s'" % line)
            self.transport.loseConnection()
            return
        
        log.msg("%s" % action)
        self._ACTIONS[action](self)
        
    def rawDataReceived(self, data):
        log.msg("[Raw Data] Received %d bytes" % len(data))
        
        self.file.write(data)
        
        if data.endswith("\r\n"):
            d.addCallBack(self.file.close)
            self.factory.doneReceiving(self.ip, self.file_path)
            
    def _sendFile(self):
        def readFile(file_path):
            self.file = open(file_path, 'rb')

            for chunk in self._readBytesFromFile(self):
                self.transport.write(chunk)
                
            """DID EVERYTHING GO SMOOTHLY?"""

            self.file.close()

        d = self.factory.getFile(self.ip)
        d.addCallback(readFile)

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
        
        self.file_path = os.path.join(
            self.factory.file_directory,
            common.random_hash())
        
        self.file = open(filename, 'wb')
        self.setRawMode()
        
    _ACTIONS = {
        "RECEIVE" : _sendFile,
        "SEND"    : _receiveFile,
        }
            
    @classmethod
    def _splitData(cls, line):

        """SPLIT DATA"""
        return line.split(_SEPARATOR)[0].strip()