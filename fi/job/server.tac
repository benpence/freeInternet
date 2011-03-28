from twisted.application import internet, service
from twisted.python import log

from fi.job.controller import JobServerController
import fi.job
import fi.job.verifier

factory = JobServerController()

application = service.Application("FreeInternet Job Server", uid=0, gid=0)
job_service = internet.TCPServer(fi.job.JOB_PORT, factory)

job_service.setServiceParent(application)