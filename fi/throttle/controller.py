from twisted.internet import protocol, reactor
from twisted.python import log

import fi
import fi.throttle
from fi.throttle.protocol import ThrottleServerProtocol, ThrottleClientProtocol
from fi.throttle.application import ThrottleApplication
from fi.throttle.model import Throttle # Specific to server

class ThrottleServerController(protocol.ServerFactory):
    protocol = ThrottleServerProtocol

    def __init__(self):
        # Start parallel loop to run pathload and get bandwidth
        ThrottleApplication.pathloadReceive()

    @classmethod
    def update(cls):
        # Get updated values
        Throttle.writeToDatabase(fi.DATABASE_PATH)
        Throttle.readIntoMemory(fi.DATABASE_PATH)
        
        # Schedule
        allocations = ThrottleApplication.schedule(
            [(client.vpn_ip,
              client.credit)
             for client in Throttle.search()])
             
        # Update memory
        Throttle.allocate(allocations)
        
        # Perform network throttling
        ThrottleApplication.throttle(allocations)
        
        # Sleep until later
        reactor.callLater(
            fi.throttle.THROTTLE_SLEEP,
            cls.update)
                
    @classmethod
    def getBandwidth(cls, ip):
        return Throttle.search(1, vpn_ip=ip).bandwidth

class ThrottleClientController(protocol.ClientFactory):
    protocol = ThrottleClientProtocol
    
    def __init__(self):
        ThrottleApplication.pathloadSend()
    
    def clientConnectionLost(self, connector, reason):
        ThrottleApplication.throttle([(fi.throttle.VPN_IP, self.allocation)])
        
        reactor.callLater(
            fi.throttle.THROTTLE_SLEEP,
            connector.connect)
    
    def allocate(self, allocation):
        self.allocation = allocation
