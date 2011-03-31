from twisted.application import internet, service
from twisted.python import log
from twisted.spread import pb

import fi
import fi.job
from fi.job.controller import JobClientController

factory = JobClientController()

application = service.Application("FreeInternet Job Client", uid=1, gid=1)
job_service = internet.TCPClient(fi.HOST, fi.job.JOB_PORT, factory)

job_service.setServiceParent(application)