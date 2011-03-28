import time

import fi.job
from fi.job.task import RemoteJob

class Repeater(RemoteJob):
    # About Task
    DESCRIPTION = "A job that waits and then outputs the input string 1000 times"
    CREDIT = 5
        
    def remote_getOutput(self, message):
        time.sleep(5)
        
        return message

    @classmethod
    def generateInput(cls):
    	while True:
    		yield "BUSY PEOPLE EAT GALAXIES"