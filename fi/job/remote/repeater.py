import time

import fi.job.remote

class Repeater(fi.job.remote.RemoteJob):
    @classmethod
    def getOutput(cls, message):
        time.sleep(5)
        
        return message

class RepeaterInput(fi.job.remote.RemoteJobInput):
    # About Task
    DESCRIPTION = "A job that waits and then repeats back you give it"
    CREDIT = 5
    
    @classmethod
    def generateInput(cls):
    	while True:
    		yield ("BUSY PEOPLE EAT GALAXIES",)
    