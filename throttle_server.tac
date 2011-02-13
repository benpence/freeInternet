import sys
sys.path.append("/home/bmp/twistedInternet/")

from twisted.application import internet, service
from twisted.python import log

import common
from throttle_controller import ThrottleServerController
import throttle_model

throttle_model.__init__()

factory = ThrottleServerController()
factory.update()

application = service.Application("FreeInternet Throttle Server", uid=0, gid=0)
job_service = internet.TCPServer(common._THROTTLE_PORT, factory)

job_service.setServiceParent(application)
