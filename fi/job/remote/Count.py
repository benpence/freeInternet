import time
import itertools

import fi.job.remote

class Count(fi.job.remote.RemoteJob):
    @classmethod
    def getOutput(cls, start, stop):
        return ' '.join(map(str, range(start, stop + 1)))

class CountInput(fi.job.remote.RemoteJobInput):
    # About Task
    DESCRIPTION = "Counts from the start to the finish"
    CREDIT = 5
    
    RANGE = 10
    
    @classmethod
    def generateInput(cls):
    	for i in itertools.count(0):
    		yield (i, i + cls.RANGE)