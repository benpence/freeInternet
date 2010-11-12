#!/usr/bin/python

import connectionClass
import socket

import threading # for threading

_BACKLOG = 5 # max number of connections; 5 is standard
_DEFAULT_HOST = ''
_DEFAULT_PORT = 5555

class Server(connectionClass.Connection):
	"""
	Server(	chunkSize=, # size of data that connection will receive
			output=) # boolean, logging printed to shell?

		listens on specified interface (IP), port for connections
		passes successful connections to ServerThread threads
	"""


	def __init__(self, **kwargs):
		super(Server, self).__init__(**kwargs)

		self.childCount = 0

	def listen(self, host=_DEFAULT_HOST, port=_DEFAULT_PORT):
		"""
		listen(	host=, # IP or domain name to listen on
				port=, # port to listen on)

			start listening for connections
			pass off connection to createThread()
		"""

		# Already listening
		if self.sock:
			self.sock.close()
			self.sock = None

		# Bind to 'host' on 'port'
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((host, port))
			self.sock.listen(_BACKLOG)

		except socket.error, (value, message): #Failed
			if self.sock:
				self.sock.close()
			self.log(	"server%03d" % self.id,
						"socket failed to listen"
						"\n\tmessage = '%s'"
						"\n\thost = '%s'"
						"\n\tport = '%s'" % (message, host, port),
						messageType = "ERR")

			return False

		self.log(		"server%03d" % self.id,
						"socket created"
						"\n\thost = '%s'"
						"\n\tport = '%s'" % (host, port))


		#Cycle through connections to service connections with data
		socketToConnection = {self.sock : self}
		connections = [sock]

		while self.running and self.sock:
			socketsToService, x, y = select.select(connections, [], [])

			for socket in socketsToService:
				# Server has new connection
				if type(socket) == type(self):
					client, address = self.sock.accept()

					self.log(	"server%03d" % self.id,
								"Creating server child"
								"\n\thost = '%s'"
								"\n\tport = '%s''" % (host, port))

					self.createChild(client, self.childCount, self)
					self.childCount += 1

				# Child connection
				else:
					socketToConnection[socket].recv()


		self.sock.close()
		self.sock = None

		return True

	def createChild(self, client, id, server):
		"""
		createChild(	client, # The client socket
						id, # A number that is unique to this child; used for logging
						server) # Reference to server process; used for logging
		"""
		pass

	def stopListen(self):
		self.running = False

class ServerChild(connectionClass.Connection):
	"""
	ServerChild(	client, # The client socket
					id, # A number that is unique to this thread; used for logging
					serverId) # Reference to server process; used for logging
	"""
	def __init__(self, client, id, serverId, **kargs):
		super(ServerChild, self).__init__(**kargs)

		self.client = client
		self.id = id
		self.serverId = serverId

	def run(self):
		pass

if __name__ == "__main__":
	server = Server()
	server.listen()
