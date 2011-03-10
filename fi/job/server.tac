from twisted.application import internet, service
from twisted.python import log

import fi
from fi.job.controller import JobServerController
import fi.job
import fi.job.model
import fi.throttle.model
import fi.job.verifier

fi.job.model.__init__()
fi.throttle.model.__init__()
fi.job.verifier.Verifier.init()

factory = JobServerController()

application = service.Application("FreeInternet Job Server", uid=0, gid=0)
job_service = internet.TCPServer(fi.job.JOB_PORT, factory)

job_service.setServiceParent(application)

class ShutdownService(service.Service):
    def startService(self):
        service.Service.startService(self)
        
    def stopService(self):
        service.Service.stopService(self)
        fi.job.model.Assign.writeToDatabase(fi.DATABASE_PATH)
        fi.job.model.Job.writeToDatabase(fi.DATABASE_PATH)
        fi.throttle.model.Throttle.writeToDatabase(fi.DATABASE_PATH)
        
shutdown_service = ShutdownService()
shutdown_service.setServiceParent(application)
