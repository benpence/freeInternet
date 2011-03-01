import sys
sys.path.append("/Users/ben/Source/freeInternet/")

from twisted.application import internet, service
from twisted.python import log

import common
from web_controller import WebController

factory = WebController()

application = service.Application("FreeInternet Throttle Server", uid=0, gid=0)
web_service = internet.TCPServer(common._WEB_PORT, factory)

web_service.setServiceParent(application)
