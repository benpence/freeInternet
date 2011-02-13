import sys
sys.path.append("/home/bmp/twistedInternet/")

from twisted.application import internet, service
from twisted.python import log

import common
from job_controller import JobServerController
import job_model
import throttle_model
import verifier

job_model.__init__()
throttle_model.__init__()
verifier.Verifier.init()

factory = JobServerController()

application = service.Application("FreeInternet Job Server", uid=0, gid=0)
job_service = internet.TCPServer(common._JOB_PORT, factory)

job_service.setServiceParent(application)

class ShutdownService(service.Service):
    def startService(self):
        service.Service.startService(self)
        
    def stopService(self):
        service.Service.stopService(self)
        job_model.Assign.writeToDatabase(common._DATABASE_PATH)
        job_model.Job.writeToDatabase(common._DATABASE_PATH)
        throttle_model.Throttle.writeToDatabase(common._DATABASE_PATH)
        
shutdown_service = ShutdownService()
shutdown_service.setServiceParent(application)
