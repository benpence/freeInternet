class RemoteJob(object):
    @classmethod
    def getOutput(cls):
        pass

class RemoteJobInput(object):
    DESCRIPTION = "Empty job"
    CREDIT = 1
    
    @classmethod
    def input(cls, MAX_JOBS):
        generator = cls.generateInput()

        for i in range(MAX_JOBS):
            yield cls.__name__, generator.next()
            
    @classmethod
    def generateInput(cls):
        pass