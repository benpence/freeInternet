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

_JOB_DIRECTORY = os.path.join(os.getcwd(), "jobs")
_OUTPUT_DIRECTORY = os.path.join(_JOB_DIRECTORY, "output")

class ServerJob(server_class.Server):
	"""

	"""
	
	def __init__(self, jobDirectory=_DEFAULT_JOB_DIRECTORY):
		self.server = fileServerClass.FileServer(filepath="workISP/test/", output=True)
		self.server.listen()

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
