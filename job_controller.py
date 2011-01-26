from twisted.application import internet, service, ILogObserver, FileLogObserver
from twisted.internet import protocol, reactor, defer
from twisted.python import log

import commands

import common
from job_model import Assign, Job

_PORT = 5555

class JobServerController(protocol.ServerFactory):
    """
    
    """
    protocol = JobProtocol
    
    getFile = assign
    doneReceiving = completeJob
    
    def assign(self, ip):
        """
        ip:str -> job_path:str
        
        Returns the path to the next job
        """
        
        job, job_instance = Assign.getNextJob()
        Assign.assign(job, job_instance, ip)
        
        log.msg("[%s] Assigning job %d %s" % (
            ip,
            job.id,
            job.job_path))
        
        return defer.succeed(job.job_path)
    
    def completeJob(self, ip, results_path):
        """
        ip:str | results_path:str -> None
        
        Verifies job that client is returning
        Marks completion in database
        """
        
        # Get relevant assignment
        assign = max(
            Assign.search(ip=ip),
            key=lambda x: x.id)
        
        if not assign:
            """HUGE ERROR EVERYBODY PANIC"""
            return
            
        cls._verifyJob(assign.id, assign.instance, results_path)
        
        Assign.complete(client, file)
        
        log.msg("[%s] Completing %d-%d %s" % (
            ip,
            assign.id,
            assign.instance,
            assign.results_path))
        
        # Get relevant job
        job = Job.search(1, id=assign.id)
        
        if not job:
            """OH FUCK OH FUCK OH FUCK"""
            return
                
        """GIVE CREDIT TO THROTTLE job.credit"""
        
    @classmethod
    def _verifyJob(cls, job_id, job_instance, results_path):
        """
        job_id:int | results_path:str -> boolean
        
        Return whether or not this job_id has been verified
        """
        
        return defer.succeed(True)

class JobClientController(protocol.ClientFactory):
    protocol = JobProtocol
    
    _FILE_DIRECTORY = "client_jobs"
    doneReceiving = doJob
    getFile = sendResults
    
    def getResults(self, ip):
        """
        ip:str -> results_path:str
        
        """
        
        return self.results_path
            
    def doJob(self, ip, job_path):
        """
        ip:str | job_path:str -> None
        
        """
        
        """ADD IN FILE CHECKING?"""
        
        # Decompress job and input data
        commands.getoutput('tar xzvf %s' % job_path)
        
        # Run job on input data
        commands.getoutput('%s/job < %s/input > %s/output' %
            tuple(3 * [self._FILE_DIRECTORY]))
        
        # Compress results
        self.filename = common._random_hash()
        self.results_path = "%s/%s" % (self._FILE_DIRECTORY, self.filename)
        
        commands.getoutput('tar cvf %s %s/output' %
            self.results_path,
            self._FILE_DIRECTORY)
        
        # Remove unnecessary files
        commands.getoutput('rm %s/job %s/input %s/output' %
            tuple(3 * [self._FILE_DIRECTORY]))

# For logging
log_file = DailyLogFile("log", "./")
application.setComponent(ILogObserver, FileLogObserver(log_file).emit)

# Start up application
application = service.Application('FreeInternet_Server', uid=1, gid=1)
factory = JobServerController()
internet.TCPServer(_PORT, factory).setServiceParent(
    service.IServiceCollection(application))

def test():
    pass

if __name__ == '__main__':
    test()