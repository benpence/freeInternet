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

	def __init__(self, **kwargs):
		super(Server, self).__init__(self, **kwargs)

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
			self.sock.listen(Server.BACKLOG)

		except socket.error, (value, message): #Failed
			if self.sock:
				self.sock.close()
			self.log("server%3d" % self.id, "socket failed to bind\n\tmessage = '%s'\n\thost = '%s'\n\tport = '%s'" % (message, host, port), messageType = "ERR")
			return False

		self.log("server%3d" % self.id, "socket created\n\thost = '%s'\n\tport = '%s'" % (host, port))
		return True

	def run(self):
		while self.running and self.sock:
			client, address = self.sock.accept()
			data = client.recv(self.chunkSize)

			if data:
				self.log("server%3d" % self.id, "data accepted\n\thost = '%s'\n\tport = '%s''" % (host, port))
				client.send(data)
				self.log("server%3d" % self.id, "sent data to client")

			client.close()

		self.sock.close()
		self.sock = None

	def close(self):
		self.running = False

if __name__ == "__main__":
	serv = Server()
	serv.bind()
	serv.start()
