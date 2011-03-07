from twisted.application import internet, service
from twisted.python import log

import freeInternet
import freeInternet.common as common
from freeInternet.web.controller import WebController

factory = WebController()

application = service.Application("FreeInternet Throttle Server", uid=1, gid=1)
web_service = internet.TCPServer(common._WEB_PORT, factory)

web_service.setServiceParent(application)