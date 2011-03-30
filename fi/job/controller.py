import commands
import sys

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
        assignment = model.Assignment.getNextJob(ip)
        model.Assignment.record(ip, assignment)
                        
        log.msg("Assignmenting %d-%d to %s" % (
            assignment.job.id,
            assignment.instance.id,
            ip
        ))
        
        return assignment.job.module, assignment.instance.input
    
    def remote_returnJob(self, ip, output):
        """
        ip:str | output:str -> None
        
        Verifies job that client is returning
        Marks completion in database
        """
        # Get relevant assignment
        assignment = model.Assignment.lookup(ip)

        assign.complete(output)
        
        log.msg("Completed %d-%d for %s" % (
            assignment.job.id,
            assignment.instance.id,
            ip,
        ))
      
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
            
    def gotJob(self, job):
        """
        job_name:Str | job_input:(_) -> None
        
        Called after job as been transferred
        """
        
        # Unpack
        name, module_input, job_input = job
        
        module = self.stringToModule(module_input, name)
        
        complete = self.tasker.callRemote(
            "returnJob",
            module.__getattribute__(name).getOutput(*job_input)
        )
        complete.addCallback(self.getJob)
    
    
    import imp
    
    @classmethod
    def stringToModule(code, name):
        """Credit: code.activestate.com/recipes/82234-importing-a-dynamically-generated-module/"""
        if name in sys.modules:
            return sys.modules[name]

        module = imp.new_module(name)

        exec code in module.__dict__
        sys.modules[name] = module

        return module