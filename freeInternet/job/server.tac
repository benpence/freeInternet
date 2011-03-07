from twisted.application import internet, service
from twisted.python import log

import freeInternet.common as common
from freeInternet.job.controller import JobServerController
import freeInternet.job.model
import freeInternet.throttle.model
import freeInternet.job.verifier

freeInternet.job.model.__init__()
freeInternet.throttle.model.__init__()
freeInternet.job.verifier.Verifier.init()

factory = JobServerController()

application = service.Application("FreeInternet Job Server", uid=0, gid=0)
job_service = internet.TCPServer(common._JOB_PORT, factory)

job_service.setServiceParent(application)

class ShutdownService(service.Service):
    def startService(self):
        service.Service.startService(self)
        
    def stopService(self):
        service.Service.stopService(self)
        freeInternet.job.model.Assign.writeToDatabase(common._DATABASE_PATH)
        freeInternet.job.model.Job.writeToDatabase(common._DATABASE_PATH)
        freeInternet.throttle.model.Throttle.writeToDatabase(common._DATABASE_PATH)
        
shutdown_service = ShutdownService()
shutdown_service.setServiceParent(application)
