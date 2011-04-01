from twisted.spread import pb
from twisted.internet import reactor

import fi

class ServerController(pb.Root):
    pass

class ClientController(pb.PBClientFactory):

    def clientConnectionMade(self, connector):
        pb.PBClientFactory.clientConnectionMade(self, connector)
        
        print "Connected to server"
        self.ip = connector.transport.getPeer().host
        self.getRoot()
        
    def clientConnectionLost(self, *args):
        self.clientConnectionFailed(*args)

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed"
        reactor.callLater(
            fi.SLEEP,
            connector.connect,
        )

        print "Reconnecting..."
        
    def _getRoot(self, *args):
        print "Receiving remote root"
        root_d = self.getRootObject()
        root_d.addCallbacks(self.gotRoot, self.gotNothing)

    def _gotNothing(self, reason):
        print "Remote call failed: " + str(reason)

    def gotRoot(self, root):
        pass