#!/usr/bin/python

"""
Server - class for listening on a port for connection
"""

from connectionClass import Connection
import socket

class Server(Connection):
	BACKLOG 		= 5 # max number of connections; 5 is standard
	DEFAULT_HOST	= ''
	DEFAULT_PORT	= 5555

	def __init__(self, backlog = Server.BACKLOG5, chunkSize = Connection.CHUNK_SIZE, output = True):
		super(Server, self).__init__(self, chunkSize = chunkSize, output = output)

		self.backlog = backlog

	# Set up for connections
	#	False 	-> Bind failed
	#	True 	-> Bind succeeded
	def bind(self, host = Server.DEFAULT_HOST, port = Server.DEFAULT_PORT):
		# Already binded?
		if self.sock:
			sock.close()

		# Bind to 'host' on 'port'
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((host, port))
			self.sock.listen(self.backlog)

		except socket.error, (value, message): #Failed
			if self.sock:
				self.sock.close()
			self.log("server%3d", "socket failed to bind\n\tmessage = '%s'\n\thost = '%s'\n\tport = '%s'\n\tbacklog = '%s'" % (self.id, message, host, port, self.backlog), visualCue = True)
			return False

		self.log("server%3d", "socket created\n\thost = '%s'\n\tport = '%s'\n\tbacklog = '%s'" % (self.id, host, port, self.backlog))
		return True

	def run(self):
		while self.running:
			pass

	def close():
		self.running = False
