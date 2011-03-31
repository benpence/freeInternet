from twisted.internet import protocol, reactor
from twisted.python import log


import fi
import fi.exception as exception
import fi.throttle
from fi.throttle.protocol import ThrottleServerProtocol, ThrottleClientProtocol
from fi.throttle.application import ThrottleApplication


try:
    import fi.throttle.model # Specific to server
except exception.OperationalError, e:
    pass


class ThrottleServerController(protocol.ServerFactory):
    protocol = ThrottleServerProtocol

    def __init__(self):
        # Start parallel loop to run pathload and get bandwidth
        ThrottleApplication.pathloadReceive()

    @classmethod
    def update(cls):
        # Get updated values
        
        # Schedule
        allocations = ThrottleApplication.schedule(
            [(client.vpn_ip,
              client.credit)
             for client in Client.query.all()])
             
        # Update memory
        Client.allocate(allocations)
        
        # Perform network throttling
        ThrottleApplication.throttle(allocations)
        
        # Sleep until later
        reactor.callLater(
            fi.throttle.SLEEP,
            cls.update
        )
                
    @classmethod
    def getBandwidth(cls, ip):
        return Client.get_by(vpn_ip=ip).bandwidth

class ThrottleClientController(protocol.ClientFactory):
    protocol = ThrottleClientProtocol
    
    def __init__(self):
        self.pathload = False
    
    def clientConnectionMade(self):
        self.ip = self.transport.getPeer()
        
        # Start once pathloading to server
        if self.ip == fi.throttle.PATHLOAD_CLIENT and not self.pathload:
            self.pathload = True
            ThrottleApplication.pathloadSend()
            
    def clientConnectionLost(self, connector, reason):
        if hasattr(self, 'allocation'):
            ThrottleApplication.throttle([(fi.throttle.VPN_IP, self.allocation)])
                    
        reactor.callLater(
            fi.throttle.SLEEP,
            connector.connect
        )
    
    def allocate(self, allocation):
        self.allocation = allocation
