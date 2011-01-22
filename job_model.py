"""
job_model.py

"""

import time

try:
	import sqlite3
except ImportError, e:
	print "'import sqlite3' failed. Using sqlite"

JobModel._read('database.db')

class JobModel(object):
	jobs = {}
	credit = {}
	
	@classmethod
	def _read(cls, database_path):
		"""
		Void -> Void
		
		Read database into memory (clientsToJob):
			clientsToJobs[client] = job
		
		"""
		
		pass
		
	def _write(cls):
		"""
		Void -> Void

		Write memory () to database
		"""
	
	@classmethod
	def assign(cls, client, job):
		clientsToJobs[client] = job

def test():
	pass


if __name__ == '__main__':
	test()