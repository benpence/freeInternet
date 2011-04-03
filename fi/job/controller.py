import commands
import sys

from twisted.python import log

import fi
import fi.controller

class JobServerController(fi.controller.ServerController):
    def __init__(self):
        import fi.job.model
        import fi.job.verifier
    
    def remote_getJob(self, ip):
        """
        ip:str -> RemoteJob
        
        Returns the path to the next job
        """
        assignment = fi.job.model.Assignment.getNextJob(ip)
        fi.job.model.Assignment.record(ip, assignment)
                        
        fi.logmsg(
            self.__class__,
            "Assigning %d-%d-%d to %s" % (
                assignment.job.id,
                assignment.instance.id,
                assignment.id,
                ip,
            )
        )
        
        return assignment.job.name, assignment.job.module, assignment.instance.input
    
    def remote_returnJob(self, ip, output):
        """
        ip:str | output:str -> None
        
        Verifies job that client is returning
        Marks completion in database
        """
        # Get relevant assignment
        assignment = fi.job.model.Assignment.lookup(ip)

        fi.job.model.Assignment.complete(ip, output)
        
        fi.logmsg(
            self.__class__,
            "Completed %d-%d-%d for %s" % (
                assignment.job.id,
                assignment.instance.id,
                assignment.id,
                ip,
            )
        )
      
        fi.job.verifier.Verifier.verify(assignment)

class JobClientController(fi.controller.ClientController):
    
    def gotRoot(self, root):
        self.root = root
        
        fi.logmsg(self.__class__, "Receiving Job")
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
            fi.logmsg(self.__class__, "Invalid job")
                        
        fi.logmsg(self.__class__, "Running %s on %s" % (name, job_input))
        module = self.stringToModule(module_input, name)
        output = module.__getattribute__(name).getOutput(*job_input)
        
        fi.logmsg(self.__class__, "Returning job output")
        complete = self.root.callRemote(
            "returnJob",
            self.ip,
            output,
        )
        
        def getAnother():
            complete.addCallbacks(
                lambda _: self.gotRoot(self.root),
                self.gotNothing
            )
            
        fi.callLater(getAnother)
    
    @classmethod
    def stringToModule(cls, code, name):
        """Credit: code.activestate.com/recipes/82234-importing-a-dynamically-generated-module/"""
        import imp
        
        if name in sys.modules:
            return sys.modules[name]

        module = imp.new_module(name)

        exec code in module.__dict__
        sys.modules[name] = module

        return module