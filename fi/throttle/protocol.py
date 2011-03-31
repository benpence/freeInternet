from twisted.protocols import basic

class ThrottleServerProtocol(basic.LineReceiver):
    def connectionMade(self):
        print "Connection"
    
    def lineReceived(self, line):
        bandwidth = self.factory.getBandwidth(line)

        print "Tell allocation: ", line, bandwidth, "kB/s"

        self.sendLine(str(bandwidth))
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        print "Disconnection"

class ThrottleClientProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.sendLine(self.factory.ip)
    
    def lineReceived(self, line):
        self.factory.allocate(str(line))
        self.transport.loseConnection()
