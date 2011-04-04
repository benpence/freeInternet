from twisted.spread import pb

import fi

class ServerController(pb.Root):
    """Remote root object called from client"""
    noisy = False

class ClientController(pb.PBClientFactory):
    """Client obtains server root object and calls its remote methods"""
    noisy = False

    def clientConnectionMade(self, connector):
        pb.PBClientFactory.clientConnectionMade(self, connector)
        
        fi.logmsg(self.__class__, "Connected to server")
        self.ip = connector.transport.getPeer().host
        self.getRoot()
        
    def clientConnectionLost(self, *args):
        self.clientConnectionFailed(*args)

    def clientConnectionFailed(self, connector, reason):
        fi.logmsg(self.__class__, "Connection lost")

        fi.callLater(connector.connect)

        fi.logmsg(self.__class__, "Reconnecting...")
        
    def getRoot(self, *args):
        """Can be called to re-get the server root object"""
        fi.logmsg(self.__class__, "Receiving remote root")
        root_d = self.getRootObject()
        root_d.addCallbacks(self.gotRoot, self.gotNothing)

    def gotNothing(self, reason):
        """For callRemote failures"""
        fi.logmsg(self.__class__, "Remote call failed: " + str(reason))

    def gotRoot(self, root):
        """Should be subclassed"""
        pass