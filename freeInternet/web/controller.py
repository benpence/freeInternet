import json

from twisted.web.server import Site

import freeInternet.common as common
from freeInternet.web.protocol import WebProtocol
import freeInternet.throttle.model

class WebController(Site):
    def __init__(self):
        Site.__init__(self, WebProtocol(self))
    
    def json(self):
        freeInternet.throttle.model.Throttle.readIntoMemory(common._DATABASE_PATH)

        clients = freeInternet.throttle.model.Throttle.search()

        credit = {}
        bandwidth = {}
        for client in clients:
            credit[client.vpn_ip] = client.credit
            bandwidth[client.vpn_ip] = client.bandwidth
    
        return json.dumps({"credit": credit, "bandwidth": bandwidth})
