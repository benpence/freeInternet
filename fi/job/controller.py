import commands
import sys

from twisted.python import log

import fi
import fi.controller

class JobServerController(fi.controller.ServerController):
    def __init__(self):
        """
        fi.*.model maps tables when loaded because there is no good class-wide init function,
        and clients do not have a database.
        """
        import fi.job.model
        import fi.job.verifier
    
    def remote_tellJob(self, ip):
        """
        ip:str -> str | str | _
        
        Gets the name, module code, and input list for the next job
        """
        assignment = fi.job.model.Assignment.nextJob(ip)
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
    
    def remote_tellOutput(self, ip, output):
        """
        ip:str | output:serializable -> None
        
        Marks completion in database
        Verifies job that client is returning
        """
        # Get relevant assignment
        assignment = fi.job.model.Assignment.lookup(ip)

        # Mark it complete in database
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
      
        # Verify returned result
        fi.job.verifier.Verifier.verify(assignment)

class JobClientController(fi.controller.ClientController):
    
    def gotRoot(self, root):
        self.root = root
        self.askJob()

    def askJob(self, *args):
        # Ask for next job
        fi.logmsg(self.__class__, "Receiving Job")
        job_d = self.root.callRemote("tellJob", self.ip)
        job_d.addCallbacks(self.toldJob, self.gotNothing)
    
    def toldJob(self, job):
        """
        job:(str, str, serializable) -> None
        
        Called after job as been transferred
        """
        
        # Unpack
        try:
            name, module_input, job_input = job
        except ValueError, e:
            fi.logmsg(self.__class__, "Invalid job")
            self.getRoot()
            return
                        
        fi.logmsg(self.__class__, "Running %s on %s" % (name, job_input))
        
        # Load module into memory from code
        module = self.stringToModule(module_input, name)
        
        # Run job
        output = module.__getattribute__(name).getOutput(*job_input)
        
        fi.logmsg(self.__class__, "Returning job output")
        complete = self.root.callRemote(
            "tellOutput",
            self.ip,
            output,
        )
        
        def askAnother():
            complete.addCallbacks(
                self.askJob,
                self.gotNothing
            )
            
        fi.callLater(askAnother)
    
    @classmethod
    def stringToModule(cls, code, name):
        """credit to: code.activestate.com/recipes/82234-importing-a-dynamically-generated-module/"""
        # Should only load the first time
        import imp
        
        if name in sys.modules:
            return sys.modules[name]

        module = imp.new_module(name)

        exec code in module.__dict__
        sys.modules[name] = module

        return module
