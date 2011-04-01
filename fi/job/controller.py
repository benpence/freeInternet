import commands
import sys

# Client
import imp

from twisted.python import log
from twisted.internet import reactor

import fi.controller
import fi.exception as exception

class JobServerController(fi.controller.ServerController):
    def __init__(self):
        import fi.job.model as model
        import fi.job.verifier
    
    def remote_getJob(self, ip):
        """
        ip:str -> RemoteJob
        
        Returns the path to the next job
        """
        assignment = model.Assignment.getNextJob(ip)
        model.Assignment.record(ip, assignment)
                        
        log.msg("Assigning %d-%d-%d to %s" % (
            assignment.job.id,
            assignment.instance.id,
            assignment.id,
            ip,
        ))
        
        return assignment.job.name, assignment.job.module, assignment.instance.input
    
    def remote_returnJob(self, ip, output):
        """
        ip:str | output:str -> None
        
        Verifies job that client is returning
        Marks completion in database
        """
        # Get relevant assignment
        assignment = model.Assignment.lookup(ip)

        model.Assignment.complete(ip, output)
        
        log.msg("Completed %d-%d-%d for %s" % (
            assignment.job.id,
            assignment.instance.id,
            assignment.id,
            ip,
        ))
      
        fi.job.verifier.Verifier.verify(assignment)
    
class JobClientController(fi.controller.ClientController):
    
    def gotRoot(self, root):
        print "Receiving Job"  
        job_d = root.callRemote("getJob", self.ip)
        job_d.addCallbacks(self.gotJob, self.gotNothing)
    
    def gotJob(self, job):
        """
        job:(str, str, (_)) -> None
        
        Called after job as been transferred
        """
        
        # Unpack
        try:
            name, module_input, job_input = job
        except ValueError, e:
            """TODO: Disconnect and get another job"""
            print "Invalid job"
                        
        print "Running %s on %s" % (name, job_input)
        
        module = self.stringToModule(module_input, name)
        
        complete = self.tasker.callRemote(
            "returnJob",
            self.ip,
            module.__getattribute__(name).getOutput(*job_input),
        )
        
        print "Returning job output"
        complete.addCallbacks(self.getJob, self.gotNothing)
    
    @classmethod
    def stringToModule(cls, code, name):
        """Credit: code.activestate.com/recipes/82234-importing-a-dynamically-generated-module/"""
        if name in sys.modules:
            return sys.modules[name]

        module = imp.new_module(name)

        exec code in module.__dict__
        sys.modules[name] = module

        return module