import commands

from twisted.python import log
from twisted.spread import pb


import fi.exception as exception
# Server
import fi.job.model as model
from fi.job.verifier import Verifier

class JobServerController(pb.Root):
    def remote_getJob(self, ip):
        """
        ip:str -> RemoteJob
        
        Returns the path to the next job
        """
        
        job = model.Assign.getNextJob(ip)
        job_name, job_input = job.input
                
        log.msg("Assigning %d to %s" % (
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
        assign = model.Assign.lookup(ip)
    
        if not assign:
            raise exception.EmptyQueryError("No assignment for completed job")

        log.msg("Completing %d-%d" % (
            assign.id,
            assign.instance))
        
        assign.complete(output)
      
        Verifier.verify(assign, output)
        
class JobClientController(pb.PBClientFactory):
    tasker = None

    def clientConnectionMade(self, connector):
        pb.PBClientFactory.clientConnectionMade(self, connector)
        
        print "Connection"
        self.ip = connector.transport.getPeer().host
        self.getJob()
        
    def getJob(self):
        def gotNothing(reason):
            raise exception.ConnectionError("Remote call failed: " + reason)
            
        def transferJob():  
            print "transferJob"  
            job_def = self.tasker.callRemote("getJob", self.ip)
            job_def.addCallbacks(self.gotJob, gotNothing)
            
        def gotTasker(tasker):
            print "gotTasker"
            print tasker
            self.tasker = tasker
            transferJob()
        
        if self.tasker:
            print "already have tasker"
            transferJob()
        else:
            print "getTasker"
            tasker_def = self.getRootObject()
            tasker_def.addCallbacks(gotTasker, gotNothing)
            
    def gotJob(self, input):
        """
        job_name:Str | job_input:(_) -> None
        
        Called after job as been transferred
        """
        job_name, job_input = input
        
        task = model.nameToJob(job_name)
        
        complete = self.tasker.callRemote(
            "returnJob",
            task.getOutput(*job_input)
        )
        complete.addCallback(self.getJob)