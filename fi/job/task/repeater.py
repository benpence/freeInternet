import time

from fi.job import Job

class Repeater(Job):
    # About Task
    DESCRIPTION = "A job that waits and then outputs the input string 1000 times"
    CREDIT = 5
        
    def getOutput(self, message):
        time.sleep(5)
        
        return message

    @classmethod
    def generateInput(cls):
    	while True:
    		yield "BUSY PEOPLE EAT GALAXIES"