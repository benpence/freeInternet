import commands

from twisted.python import log
from twisted.spread import pb

import fi.exception as exception
# Server
import fi.job.model
from fi.job.model import Assign, Job
from fi.job.verifier import Verifier

class JobServerController(pb.Root):
    def remote_getJob(self, ip):
        """
        ip:str -> RemoteJob
        
        Returns the path to the next job
        """
        
        job_name, job_input = Assign.getNextJob(ip)
                
        log.msg("Assigning job %d to %s" % (
            job.id,
            ip
        ))
        
        return job_name, job_input
    
    def remote_returnJob(self, ip, output):
        """
        ip:str | output:str -> None
        
        Verifies job that client is returning
        Marks completion in database
        """
        
        # Get relevant assignment
        assign = Assign.lookup(ip)
    
        if not assign:
            raise exception.EmptyQueryError("No assignment for completed job")

        log.msg("Completing %d-%d" % (
            assign.id,
            assign.instance))
        
        assign.complete(output)
      
        Verifier.verify(assign, output)
        
class JobClientController(pb.PBClientFactory):
    def clientConnectionMade(self):
        self.getJob()
        
    def getJob(self):
        def doJob():    
            job_def = self.tasker.callRemote("getJob", self.ip)
            job_def.addCallback(self.gotJob)
            
        def gotTasker(tasker):
            self.tasker = tasker
            doJob()
            
        if self.tasker:
            doJob()
        else:
            tasker_def = factory.getRootObject()
            tasker_def.addCallback(gotTasker)
            
    def gotJob(self, job_name, job_input):
        """
        job_name:Str | job_input:(_) -> None
        
        Called after job as been transferred
        """
        
        task = __import__('fi.job.task').__getAttribute__(job_name)
        
        complete = self.tasker.callRemote(
            "returnJob",
            task.getOutput(*job_input)
        )
        complete.addCallback(self.getJob)