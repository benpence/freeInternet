import sys
sys.path.append("/Users/ben/Source/twisted/")

from twisted.application import internet, service
from twisted.python import log

import common
from throttle_controller import ThrottleClientController

factory = ThrottleClientController()

application = service.Application("FreeInternet Throttle Client", uid=1, gid=1)
throttle_service = internet.TCPClient(common._HOST, common._JOB_PORT, factory)

throttle_service.setServiceParent(application)