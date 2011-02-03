import sys
sys.path.append("/Users/ben/Source/twisted/")

from twisted.application import internet, service
from twisted.python import log

import common
from job_controller import JobServerController
import job_model

job_model.__init__()

factory = JobServerController()

application = service.Application("FreeInternet Server", uid=1, gid=1)
job_service = internet.TCPServer(common._PORT, factory)

job_service.setServiceParent(application)

class ShutdownService(service.Service):
    def startService(self):
        service.Service.startService(self)
        
    def stopService(self):
        service.Service.stopService(self)
        job_model.Assign.writeToDatabase(common._DATABASE_PATH)
        job_model.Job.writeToDatabase(common._DATABASE_PATH)
        
shutdown_service = ShutdownService()
shutdown_service.setServiceParent(application)