#!/usr/bin/python

"""
workISP
	sends jobs to the clients
	receives results from the clients
	verifies results from the clients
"""

#Add helper libraries

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
        super(Server, self).__init__(jobDirectory=_JOB_DIRECTORY)

		self.listen()

    def getJobID(self):
        return 0011

    def __str__(self):
        return "workServer"

	def log(self, *args, **kargs):
		if 'output' not in kargs:
			kargs['output'] = self.output

		logging.Logger.log(*args, **kargs)

def Main():
    server = Server(jobDirectory=_JOB_DIRECTORY)
    server.listen()
	server = WorkServer()

if __name__ == "__main__":
	Main()
