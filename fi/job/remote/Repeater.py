import time

import fi.job.remote

class Repeater(fi.job.remote.RemoteJob):
    @classmethod
    def getOutput(cls, message):
        return message

class RepeaterInput(fi.job.remote.RemoteJobInput):
    # About Task
    DESCRIPTION = "Waits and then repeats back what you give it"
    CREDIT = 5
    
    @classmethod
    def generateInput(cls):
    	while True:
    		yield ("BUSY PEOPLE EAT GALAXIES",)
    