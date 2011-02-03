import commands

from twisted.internet import protocol
from twisted.python import log

import common
from job_protocol import JobServerProtocol, JobClientProtocol
from job_model import Assign, Job # Specific to server
from job_client import JobClient # Specific to client
from verifier import Verifier


class JobServerController(protocol.ServerFactory):
    """
    
    """
    protocol = JobServerProtocol
    file_directory = common._SERVER_DIRECTORY
    
    @classmethod
    def assign(cls, ip):
        """
        ip:str -> job_path:str
        
        Returns the path to the next job
        """
        
        job, job_instance = Assign.getNextJob(ip)
        Assign.assign(job, job_instance, ip)
        
        log.msg("Assigning job %d-%d" % (
            job.id,
            job_instance))
        
        return job.job_path
    getFile = assign
    
    @classmethod
    def completeJob(cls, ip, results_path):
        """
        ip:str | results_path:str -> None
        
        Verifies job that client is returning
        Marks completion in database
        """
        
        # Get relevant assignment
        assign = max(
            Assign.search(ip=ip),
            key=lambda x: int("%d%d" % (x.id, x.instance)))
        
        if not assign:
            """HUGE ERROR EVERYBODY PANIC"""
            return
            
        cls._verifyJob(assign.id, assign.instance, results_path)
        
        Assign.complete(ip, results_path)
        
        log.msg("Completing %d-%d" % (
            assign.id,
            assign.instance))
        
        # Get relevant job
        job = Job.search(1, id=assign.id)
        
        if not job:
            """OH FUCK OH FUCK OH FUCK"""
            return
                
    doneReceiving = completeJob
       
    @classmethod
    def _verifyJob(cls, job_id, job_instance, results_path):
        """
        job_id:int | job_instance:int | results_path:str -> boolean
        
        Return whether or not this job_id has been verified
        """
        
        Verifier.verify(job_id, job_instance, results_path)

class JobClientController(protocol.ClientFactory):
    """
    
    """
    protocol = JobClientProtocol
    file_directory = common._CLIENT_DIRECTORY
    
    def __init__(self):
        self.gettingJob = True
        
    def clientConnectionMade(self):
        if self.gettingJob:
            print "Getting new job"
            self.action = "SEND"
            
        else:
            print "Sending results"
            self.action = "RECEIVE"
    
    def clientConnectionLost(self, connector, reason):
        # Do job if in gettingJob mode
        if self.gettingJob:
            self.results_path, shell = JobClient.doJob(self.job_path)
            self.gettingJob = not self.gettingJob
            shell.callStack.addCallback(lambda s: connector.connect())
        else:
            self.gettingJob = not self.gettingJob
            connector.connect()

    def gotJob(self, ip, job_path):
        """
        ip:str | job_path:str -> None
        
        Called after job as been transferred
        """
                
        self.job_path = job_path
    doneReceiving = gotJob
    
    def getResultsPath(self, ip):
        """
        ip:str -> results_path:str

        Called to get the results_path to transfer
        """
        
        return self.results_path
    getFile = getResultsPath

        
def test():
    pass

if __name__ == '__main__':
    test()