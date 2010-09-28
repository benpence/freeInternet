#!/usr/bin/python

"""
Server - class for listening on a port for connection
"""

from connectionClass import Connection
import socket

from threading import Thread	# for threading

BACKLOG 		= 5 # max number of connections; 5 is standard
DEFAULT_HOST	= ''
DEFAULT_PORT	= 5555

class Server(Connection):

	def __init__(self, **kwargs):
		super(Server, self).__init__(**kwargs)

		self.threadCount = 0

	# Set up for connections
	#	False 	-> Bind failed
	#	True 	-> Bind succeeded
	def bind(self, host = DEFAULT_HOST, port = DEFAULT_PORT):
		# Already binded?
		if self.sock:
			self.sock.close()
			self.sock = None

		# Bind to 'host' on 'port'
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((host, port))
			self.sock.listen(BACKLOG)

		except socket.error, (value, message): #Failed
			if self.sock:
				self.sock.close()
			self.log("server%03d" % self.id, "socket failed to bind\n\tmessage = '%s'\n\thost = '%s'\n\tport = '%s'" % (message, host, port), messageType = "ERR")
			return False

		self.log("server%03d" % self.id, "socket created\n\thost = '%s'\n\tport = '%s'" % (host, port))


		# Running loop #
		print "Running = ", self.running
		while self.running and self.sock:
			client, address = self.sock.accept()
			data = client.recv(self.chunkSize)

			if data:
				self.log("server%03d" % self.id, "data accepted. Creating server thread\n\thost = '%s'\n\tport = '%s''" % (host, port))

				newThread = ServerThread(client, data, self.threadCount, self)
				self.threadCount += 1

				newThread.start()

		self.sock.close()
		self.sock = None

		return True

	def close(self):
		self.running = False

class ServerThread(Thread):
	def __init__(self, sock, data, id, parent):
		self.sock = sock
		self.id = id
		self.data = data
		self.parent = parent

		Thread.__init__(self)

	def run(self):
		self.sock.send(self.data)
		self.parent.log("server%03d" % self.parent.id, "thread%03d sent '%s' to client" % (self.id, self.data))

		self.sock.close()

if __name__ == "__main__":
	serv = Server()
	serv.bind()
