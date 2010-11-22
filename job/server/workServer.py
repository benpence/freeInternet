#!/usr/bin/python

"""
workISP
	sends jobs to the clients
	receives results from the clients
	verifies results from the clients
"""

#Add helper libraries
import sys

sys.path.insert(0, "../helper")
from constants import _ROOT_DIRECTORY #Root directory
from logging import Logger	#Logger class
import fileServerClass #FileServer class

_DEFAULT_JOB_DIRECTORY = "%sworkISP/test/" % _ROOT_DIRECTORY

class WorkServer:
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
	server = WorkServer()

if __name__ == "__main__":
	Main()
