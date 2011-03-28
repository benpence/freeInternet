from twisted.spread import pb

from diffie_hellman import DiffieHellman
from repeater import Repeater

class RemoteJob(pb.Referenceable):
    DESCRIPTION = ""
    CREDIT = 0

    @classmethod
    def input(cls):
        generator = cls.generateInput()
        
        for i in range(fi.job.MAX_JOBS):
            yield cls.__name__, generator.next()

    @classmethod
    def remote_getOutput(cls):
        pass
    
    @classmethod
    def generateInput(cls):
        pass
