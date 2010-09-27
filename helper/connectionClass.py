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

	def __init__(self, chunkSize = Connection.CHUNK_SIZE):

		self.chunkSize = chunkSize

		self.running = True						# for threading
		self.sock = None						# socket

		self.id = Connection.count				# identifier for logging
		Connection.count += 1
		Connection.intances[self.id] = self		# singleton

	def close(self):
		pass

	def log(*args):
		Logger.log(args, self.output)
