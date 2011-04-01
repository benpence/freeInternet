from twisted.python import log

import fi
import fi.controller
import fi.throttle
from fi.throttle.application import ThrottleApplication

class ThrottleServerController(fi.controller.ServerController):

    def __init__(self):
        import fi.throttle.model as model

    def rootObject(self, broker):
        """
        Called when a broker publishes me me
        """
        # Get available bandwidth
        ThrottleApplication.pathloadReceive()
        self.update()

    @classmethod
    def update(cls):
        # Schedule
        credits = []
        
        for client in model.Client.query.all():
            credits.append((client.vpn_ip, client.credit))
    
        allocations = ThrottleApplication.schedule(credits)
     
        # Update memory
        model.Client.allocate(allocations)
        
        # Perform network throttling
        ThrottleApplication.throttle(allocations)
        
        # Sleep until later
        reactor.callLater(
            fi.SLEEP,
            cls.update
        )

    def remote_getBandwidth(self, ip):
        return model.Client.get_by(ip=ip).bandwidth

class ThrottleClientController(fi.controller.ClientController):

    def gotRoot(self, root):
        # Start once pathloading to server
        ThrottleApplication.pathloadSend()
        
        bandwidth_d = root.callRemote(
            "getBandwidth",
            self.ip
        )
        
        bandwidth_d.addCallbacks(
            lambda bandwidth: ThrottleApplication.throttle((fi.throttle.VPN_SERVER_IP, bandwidth)),
            self.gotNothing
        )