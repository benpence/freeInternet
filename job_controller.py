import commands

from twisted.internet import protocol, defer
from twisted.python import log

import common
from job_model import Assign, Job
from job_protocol import JobProtocol

class JobServerController(protocol.ServerFactory):
    """
    
    """
    protocol = JobProtocol
    
    @classmethod
    def assign(cls, ip):
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
            key=lambda x: x.id)
        
        if not assign:
            """HUGE ERROR EVERYBODY PANIC"""
            return defer.succeed()
            
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
            return defer.succeed()
                
        """GIVE CREDIT TO THROTTLE job.credit"""
    doneReceiving = completeJob
        
    @classmethod
    def _verifyJob(cls, job_id, job_instance, results_path):
        """
        job_id:int | results_path:str -> boolean
        
        Return whether or not this job_id has been verified
        """
        
        return defer.succeed(True)

class JobClientController(protocol.ClientFactory):
    protocol = JobProtocol
        
    

    @classmethod
    def getAssignment(cls):
        """
        None -> None
        
        Initiates connection to server to get assignment
        """
    
    def sendResults(cls):
        """"""
    
    @classmethod
    def doneReceiving(cls, ip, job_path):
        """
        ip:str | job_path:str -> None
        
        Called after job as been transferred
        """
        
        cls.job_path = job_path

    @classmethod
    def getResultsPath(cls, ip):
        """
        ip:str -> results_path:str

        Called to get the results_path to transfer
        """

        return cls.results_path
    getFile = getResultsPath
        
def test():
    pass

if __name__ == '__main__':
    test()