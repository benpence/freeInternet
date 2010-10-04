#!/usr/bin/python

import connectionClass
import socket

class Client(connectionClass.Connection):
	"""
	Client(	chunkSize=, # size of data that connection will receive
			output=) # boolean, logging printed to shell?
	"""

	_DEFAULT_HOST = 'localhost'
	_DEFAULT_PORT = 5555

	def __init__(self, **kwargs):
		super(Client, self).__init__(**kwargs)

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
						"failed to connect"
						"\n\tmessage = '%s'"
						"\n\thost = '%s'"
						"\n\tport = '%s'" % (message, host, port),
						messageType="ERR")
			return False

		self.log(	"client%03d" % self.id,
					"socket connected"
					"\n\thost = '%s'"
					"\n\tport = '%s'" % (host, port))

		self.connectActions()

		self.sock.close()
		self.sock = None

		return True

	def connectActions(self):
		pass

if __name__ == "__main__":
	cli = Client()
	cli.connect()
