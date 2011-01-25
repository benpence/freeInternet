from twisted.protocols import basic
from twisted.python import log

from job_controller import JobServerController, JobClientController

class JobServerProtocol(basic.LineReceiver):
    _ACTIONS = {
        "ASSIGN"   : lambda x: x._readFile,
        "COMPLETE" : lambda x: x._writeFile
        }

    def connectionMade(self):
        self.ip = self.transport.getPeer().host
        log.msg("[%s] New Connection" % self.ip)
        
    def connectionLost(self, reason):
        log.msg("[%s] Connection Lost" % self.ip)
                
    def lineReceived(self, line):
        try:
            action, filesize = self._splitData(line)
        except TypeError,
            log.msg("%s][Action] Invalid Action '%s'" % (self.ip, line))
            self.transport.loseConnection()
            return
        
        if action not in self._ACTIONS or not self._isNumber(filesize):
            log.msg("%s][Action] Invalid Action '%s'" % (self.ip, line))
        else:
            log.msg("[%s] %s %d" % (self.ip, action, filesize))
            self._ACTIONS[action](filesize)

        self.transport.loseConnection()        
        
    def rawDataReceived(self, data):
        log.msg("[%s][Raw Data] Received %d bytes" % (self.ip, len(data)))
        self.file.write()
        print self, data
    
    @classmethod
    def _splitData(cls, data):
        
        """SPLIT DATA"""
        
        return data
        
    def _receiveFile(self):
        """Sets up protocol to receive a file"""
        self.filepath = 
        self.file = open(filepath, 'rb')
        
        """RECEIVE FILE"""
        
        self.factory.completeJob(self.ip, self.file)
        
    def _sendFile(self):
        self.filepath = JobServerController.getNewJob()
        d = self.factory.getNewJob(self.ip)
        
        
        def sendFile(file):
            self.file = open(filepath, 'wb')
            
            for chunk in self._readBytesFromFile(self):
                self.
            
            self.file.close()
                
        d.addCallback(sendFile)
        d.addErrback(lambda err: print err)
        """SEND FILE"""
    
    def _readBytesFromFile(self):
        while True:
            chunk = self.file.read(chunk_size)

            if chunk:
                yield chunk
            else:
                break

    @classmethod    
    def _isNumber(cls, number):
        return isinstance(number, (int, long, float, complex))

class JobClientProtocol(basic.LineReceiver):

    def connectionMade(self):
        ip = self.transport.getPeer().host
        print self, ip

    def connectionLost(self, reason):
        self.

    def lineReceived(self, line):
        print self, line

    def rawDataReceived(self, data):
        print self, data

    def _receiveFile(self):
        """Sets up protocol to receive a file"""
        self.file = str(filename)

    def _sendFile(self):
        self.type == "server":
            self.file = JobServerController.getNextJob()    
    

    
