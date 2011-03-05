import json

from twisted.web.server import Site
import common

from web_protocol import WebProtocol
import throttle_model

class WebController(Site):
    def __init__(self):
        Site.__init__(self, WebProtocol(self))
    
    def json(self):
        throttle_model.Throttle.readIntoMemory(common._DATABASE_PATH)

        clients = throttle_model.Throttle.search()

        credit = {}
        bandwidth = {}
        for client in clients:
            credit[client.vpn_ip] = client.credit
            bandwidth[client.vpn_ip] = client.bandwidth
    
        return json.dumps({"credit": credit, "bandwidth": bandwidth})
