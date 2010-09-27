#!/usr/bin/python

"""
Connection - class for listening on a port for connection
"""

#Add helper libraries
import sys

sys.path.insert(0, "../helper")
from logging import Logger	#Logger class

from threading import Thread	# for threading

class Connection(Thread):
	CHUNK_SIZE = 4096

	instances = {}
	count = 0

	def __init__(self, chunkSize = CHUNK_SIZE, output = True):
		Thread.__init__(self)

		self.chunkSize = chunkSize
		self.output = output

		self.running = True						# for threading
		self.sock = None						# socket

		self.id = Connection.count				# identifier for logging
		Connection.count += 1
		Connection.instances[self.id] = self	# singleton

	def close(self):
		pass

	def log(self, *args, **kargs):
		# If not specified, go by the object's default value for visualCue (output)
		if 'visualCue' not in kargs:
			kargs['visualCue'] = self.output
		Logger.log(*args, **kargs)

if __name__ == "__main__":
	hey = Connection()
	hey.log("program", "THIS IS A TEST", visualCue = True)
