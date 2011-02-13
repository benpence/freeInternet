from twisted.internet import protocol, reactor
from twisted.python import log

import common
from throttle_protocol import ThrottleServerProtocol, ThrottleClientProtocol
from throttle_application import ThrottleApplication
from throttle_model import Throttle # Specific to server

class ThrottleServerController(protocol.ServerFactory):
    protocol = ThrottleServerProtocol

    @classmethod
    def update(cls):
        # Get updated values
        Throttle.writeToDatabase(common._DATABASE_PATH)
        Throttle.readIntoMemory(common._DATABASE_PATH)
        
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
            common._THROTTLE_SLEEP,
            cls.update)
                
    @classmethod
    def getBandwidth(cls, ip):
        return Throttle.search(1, vpn_ip=ip).bandwidth

class ThrottleClientController(protocol.ClientFactory):
    protocol = ThrottleClientProtocol
    
    def clientConnectionLost(self, connector, reason):
        ThrottleApplication.throttle([(common._IP, self.allocation)])
        
        reactor.callLater(
            common._THROTTLE_SLEEP,
            connector.connect)
    
    def allocate(self, allocation):
        self.allocation = allocation
