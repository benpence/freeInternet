import sys
sys.path.append('/media/home/Source/freeInternet')
from twisted.application import internet, service
from twisted.python import log
from twisted.spread import pb

from fi.job.controller import JobServerController
import fi.job
import fi.job.verifier

factory = pb.PBServerFactory(JobServerController())

application = service.Application("FreeInternet Job Server", uid=1, gid=1)
job_service = internet.TCPServer(fi.job.JOB_PORT, factory)

job_service.setServiceParent(application)