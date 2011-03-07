from twisted.application import internet, service
from twisted.python import log

import freeInternet.common as common
from freeInternet.job.controller import JobClientController


factory = JobClientController()

application = service.Application("FreeInternet Job Client", uid=1, gid=1)
job_service = internet.TCPClient(common._HOST, common._JOB_PORT, factory)

job_service.setServiceParent(application)