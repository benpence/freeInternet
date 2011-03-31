from twisted.application import internet, service
from twisted.python import log

import fi
import fi.job
from fi.throttle.controller import ThrottleClientController

factory = ThrottleClientController()

application = service.Application("FreeInternet Throttle Client", uid=1, gid=1)
throttle_service = internet.TCPClient(fi.HOST, fi.job.JOB_PORT, factory)

throttle_service.setServiceParent(application)