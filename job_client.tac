import sys
sys.path.append("/Users/ben/Source/twisted/")

from twisted.application import internet, service
from twisted.python import log

import common
from job_controller import JobClientController


factory = JobClientController()

application = service.Application("FreeInternet Client", uid=1, gid=1)
job_service = internet.TCPClient(common._HOST, common._PORT, factory)

job_service.setServiceParent(application)

from job_controller import JobClientController