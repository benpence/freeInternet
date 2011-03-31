import commands
import sys

# Client
import imp
import time

from twisted.python import log
from twisted.spread import pb

import fi.exception as exception


# Server
try:
    import fi.job.model as model
    import fi.job.verifier
except exception.OperationalError, e:
    pass
    
class JobServerController(pb.Root):
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
        
class JobClientController(pb.PBClientFactory):
    tasker = None

    def clientConnectionMade(self, connector):
        pb.PBClientFactory.clientConnectionMade(self, connector)
        
        print "Connected to server"
        self.ip = connector.transport.getPeer().host
        self.getJob()

    def clientConnectionLost(self, *args):
        self.clientConnectionFailed(*args)

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed"
        time.sleep(2)
        print "Reconnecting..."
        connector.connect()
        #raise exception.ConnectionError("Remote call failed: " + reason)
        
    def gotNothing(self, reason):
        print "Remote call failed: " + str(reason)
        
    def getJob(self, *args):
        def transferJob():  
            print "Receiving Job"  
            job_def = self.tasker.callRemote("getJob", self.ip)
            job_def.addCallbacks(self.gotJob, self.gotNothing)
            
        def gotTasker(tasker):
            self.tasker = tasker
            transferJob()

        print "Receiving remote scheduler"
        tasker_def = self.getRootObject()
        tasker_def.addCallbacks(gotTasker, self.gotNothing)
            
    def gotJob(self, job):
        """
        job_name:Str | job_input:(_) -> None
        
        Called after job as been transferred
        """
        # Unpack
        name, module_input, job_input = job
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