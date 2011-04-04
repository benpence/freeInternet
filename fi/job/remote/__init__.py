class RemoteJob(object):
    """Interface for a RemoteJob"""
    @classmethod
    def getOutput(cls):
        """
        *serializable -> serializable
        
        Get outp
        This MUST MUST MUST return a serializable object
        """
        pass

class RemoteJobInput(object):
    """Abstract class for generating inputs for RemoteJob"""
    DESCRIPTION = "Empty job"
    CREDIT = 1
    INPUT = ""
    OUTPUT = ""
    
    @classmethod
    def input(cls, instances):
        """
        instances:int -> serializable
        """
        generator = cls.generateInput()

        for i in range(instances):
            yield generator.next()
            
    @classmethod
    def generateInput(cls):
        """
        None -> serializable
        
        Overridden by a generating function for job instance input
        This MUST MUST MUST return a serializable object
        """
        pass