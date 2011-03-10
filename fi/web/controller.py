import json

from twisted.web.server import Site

import fi
from fi.web.protocol import WebProtocol
import fi.throttle.model

class WebController(Site):
    def __init__(self):
        Site.__init__(self, WebProtocol(self))
    
    def json(self):
        fi.throttle.model.Throttle.readIntoMemory(fi.DATABASE_PATH)

        clients = fi.throttle.model.Throttle.search()

        credit = {}
        bandwidth = {}
        for client in clients:
            credit[client.vpn_ip] = client.credit
            bandwidth[client.vpn_ip] = client.bandwidth
    
        return json.dumps({"credit": credit, "bandwidth": bandwidth})
