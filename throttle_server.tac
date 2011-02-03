import sys
sys.path.append("/Users/ben/Source/twisted/")

from twisted.application import internet, service
from twisted.python import log

import common
import throttle_model

throttle_model.__init__()

factory = ThrottleServerController()

application = service.Application("FreeInternet Throttle Server", uid=1, gid=1)
job_service = internet.TCPServer(common._THROTTLE_PORT, factory)

job_service.setServiceParent(application)