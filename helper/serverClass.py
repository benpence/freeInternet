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

		self.threadCount = 0

	def bind(self, host=_DEFAULT_HOST, port=_DEFAULT_PORT):
		"""
		Set up for connections
		 	False 	-> Bind failed
			True 	-> Bind succeeded
		"""

		# Already binded?
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
						"socket failed to bind\n\t"
						"message = '%s'\n\t"
						"host = '%s'\n\t"
						"port = '%s'" % (message, host, port),
						messageType = "ERR")

			return False

		self.log(		"server%03d" % self.id,
						"socket created\n\t"
						"host = '%s'\n\t"
						"port = '%s'" % (host, port))

		while self.running and self.sock:
			client, address = self.sock.accept()
			data = client.recv(self.chunkSize)

			if data:
				self.log(	"server%03d" % self.id,
							"data accepted. Creating server thread\n\t"
							"host = '%s'\n\t"
							"port = '%s''" % (host, port))

				self.createThread(client, data, self.threadCount, self)
				self.threadCount += 1

		self.sock.close()
		self.sock = None

		return True

	def createThread(self, client, data, id, server):
		pass

	def close(self):
		self.running = False

class ServerThread(threading.Thread):
	"""
	ServerThread(	client, # The client socket
					data, # The data sent across the socket
					id, # A number that is unique to this thread; used for logging
					server) # Reference to server process; used for logging
	"""
	def __init__(self, client, data, id, server):
		self.client = client
		self.id = id
		self.data = data
		self.server = server

		threading.Thread.__init__(self)

	def run(self):
		pass

if __name__ == "__main__":
	serv = Server()
	serv.bind()
	serv.run()
