from twisted.python import log

import fi
import fi.controller
import fi.throttle
from fi.throttle.application import ThrottleApplication

class ThrottleServerController(fi.controller.ServerController):

    def __init__(self):
        import fi.throttle.model

    @classmethod
    def update(cls):
        # Schedule
        credits = []
        
        for client in fi.throttle.model.Client.query.all():
            credits.append((client.vpn_ip, client.credit))
    
        allocations = ThrottleApplication.schedule(credits)
     
        # Update memory
        fi.throttle.model.Client.allocate(allocations)
        
        # Perform network throttling
        ThrottleApplication.throttle(allocations)

    def remote_tellBandwidth(self, ip):
        bandwidth = fi.throttle.model.Client.get_by(ip=ip).bandwidth
        fi.logmsg(self.__class__, "Tell %s %dkbps" % (ip, bandwidth))
        return bandwidth

class ThrottleClientController(fi.controller.ClientController):

    def gotRoot(self, root):
        self.root = root
        # Start once pathloading to server
        ThrottleApplication.pathloadSend()
        
        fi.callLater(self.askBandwidth)
        
    def askBandwidth(self):
        fi.logmsg(self.__class__, "Ask bandwidth")
        bandwidth_d = self.root.callRemote(
            "tellBandwidth",
            self.ip
        )
        
        bandwidth_d.addCallbacks(
            self.toldBandwidth,
            self.gotNothing,
        )

    def toldBandwidth(self, bandwidth):
        fi.logmsg(self.__class__, "Told %dkbps" % bandwidth)

        ThrottleApplication.throttle(
            ((fi.throttle.VPN_SERVER_IP, bandwidth),)
        )
                
        self.gotRoot(self.root)