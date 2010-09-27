#!/usr/bin/python

"""
Client - class for connecting on a port for connection
"""

from connectionClass import Connection
import socket

class Client(Connection):
	DEFAULT_HOST = 'localhost'
	DEFAULT_PORT = 5556

	def __init__(self, chunkSize = Connection.CHUNK_SIZE, output = True):
		super(Client, self).__init__(self, chunkSize = chunkSize, output = output)

	# Set up connection to server
	#	False 	-> Connection failed
	#	True 	-> Connection succeeded
	def connect(self, host = Client.DEFAULT_HOST, port = Client.DEFAULT_PORT):
		# Already connected?
		if self.sock:
			sock.close()

		# Connect to server
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((host, port))

		except socket.error, (value, message): #Failed
			if self.sock:
				self.sock.close()

			self.log("client%3d", "failed to connect\n\tmessage = '%s'\n\thost = '%s'\n\tport = '%s'" % (self.id, message, host, port))
			return False

		self.log("client%3d", "socket connected\n\thost = '%s'\n\tport = '%s'" % (self.id, host, port))
		return True
	
	def sendFile(filename, path = None, host = self.host, port = self.port):
		pass
