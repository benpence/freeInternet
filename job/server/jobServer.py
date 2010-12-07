#!/usr/bin/python

import os

import sys
sys.path.insert(0, "../../classes")
import server_class

class ServerJob(server_class.Server):
    """
        TESTTEST
    """

    _JOB_DIRECTORY = os.path.join(os.getcwd(), "jobs")
    
    def __init__(self):
        super(server_class.Server, self).__init__(jobDirectory=_JOB_DIRECTORY)

        self.listen()

    def getJobID(self):
        return 0011

    def __str__(self):
        return "jobServer"

    #def log(self, *args, **kargs):
        #if 'output' not in kargs:
            #kargs['output'] = self.output
#
        #logging.Logger.log(*args, **kargs)

def Main():
    server = ServerJob()
    server.listen()

if __name__ == "__main__":
    Main()
