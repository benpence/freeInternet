from twisted.application import internet, service, ILogObserver, FileLogObserver
from twisted.internet import protocol, reactor, defer
from twisted.python import log

from job_model import Assign, Job

_PORT = 5555

class JobServerController(protocol.ServerFactory):
    protocol = JobServerProtocol
    
    @classmethod
    def assign(cls, ip):
        """
        ip:str -> job_path:str
        
        Returns the path to the job file to transfer for ip
        """
        
        d = Assign.getNextJob()
        
        def assignJob(job, job_instance):
            Assign.assign(job, job_instance, ip)
        
    
    @classmethod
    def completeJob(cls, ip, file):
        """ip (str), File -> Bool"""
        
        if cls._verifyJob(client, file):
            JobModel.complete(client, file)
            return True
        else:
            return None
        
    @classmethod
    def _verifyJob(cls, client):
        """Client -> Bool"""
        
        return True

    @classmethod    
    def _isAssigned(cls, client):
        """Client -> Bool"""

        return cls._lookupJob(client) is not None
                
    @classmethod    
    def _lookupJob(cls, ip):
        """Client -> Job"""
        
        return Assign.lookupJob(ip)


class JobClientController(protocol.ClientFactory):
    protocol = JobClientProtocol

# For logging
log_file = DailyLogFile("log", "./")
application.setComponent(ILogObserver, FileLogObserver(log_file).emit)

# Start up application
application = service.Application('FreeInternet_Job_Server', uid=1, gid=1)
factory = JobServerController()
internet.TCPServer(_PORT, factory).setServiceParent(
    service.IServiceCollection(application))

def test():
    pass

if __name__ == '__main__':
    test()