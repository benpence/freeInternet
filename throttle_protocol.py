from twisted.protocols import basic

import common

class ThrottleServerProtocol(basic.LineReceiver):
    def connectionMade(self):
        print "Connection"
    
    def lineReceived(self, line):
        self.sendLine(
            str(self.factory.getBandwidth(line)))
        self.transport.loseConnection()
    
    def connectionLost(self):
        print "Disconnection"

class ThrottleClientProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.sendLine(self.factory.ip)
    
    def lineReceived(self, line):
        self.factory.allocate(
            str(line))
        self.transport.loseConnection()