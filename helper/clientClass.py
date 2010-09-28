#!/usr/bin/python

import connectionClass
import socket

from threading import Thread	# for threading

class Client(connectionClass.Connection, Thread):
	"""
	Client(	chunkSize=, # size of data that connection will receive
			output=) # boolean, logging printed to shell?

		
	"""

	_DEFAULT_HOST = 'localhost'
	_DEFAULT_PORT = 5555

	def __init__(self, **kwargs):
		super(Client, self).__init__(**kwargs)

		self.queue = []

	def connect(self, host=_DEFAULT_HOST, port=_DEFAULT_PORT):
		"""
		Set up connection to server
			False 	-> Connection failed
			True 	-> Connection succeeded
		"""

		# Already connected?
		if self.sock:
			self.sock.close()
			self.sock = None

		# Connect to server
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((host, port))

		except socket.error, (value, message): #Failed
			if self.sock:
				self.sock.close()

			self.log(	"client%03d" % self.id,
						"failed to connect\n\t"
						"message = '%s'\n\t"
						"host = '%s'\n\t"
						"port = '%s'" % (message, host, port),
						messageType="ERR")
			return False

		self.log(	"client%03d" % self.id,
					"socket connected\n\t"
					"host = '%s'\n\t"
					"port = '%s'" % (host, port))

		# File transfer
		while self.running and len(self.queue) > 0:
			if self.sock:

				# Returns true on successful send, otherwise try send again
				if self.__sendFileFromQueue(self.queue[0]):
					self.queue.pop(0)

		self.sock.close()
		self.sock = None

		return True

	def sendFile(self, filepath):
		self.queue.append(filepath)

	def __sendFileFromQueue(self, filepath):
		self.sock.send(filepath)
		data = self.sock.recv(self.chunkSize)

		self.log(	"client%03d" % self.id,
					"sent '%s\n\t"
					"received '%s'" % (filepath, data))
		return True

	def close(self):
		self.running = False

if __name__ == "__main__":
	cli = Client()
	cli.sendFile("Hello, world")
	cli.connect()
