#!/usr/bin/python

"""
Server - class for listening on a port for connection
"""

#Add helper libraries
import sys

sys.path.insert(0, "../helper")
from logging import Logger	#Logger class

import socket

class Server:
	servers = {}
	count = 0

	def __init__(self, host = '', port = 5555, backlog = 5, receiveSize = 1024):
		self.host = host
		self.port = port
		self.backlog = backlog 			#max number of connections; 5 is standard
		self.running = True				#for shutting down later

		self.id = Client.count			#server identifier for logging
		Client.count += 1				
		Server.servers[self.id] = self	#singleton

	# Set up for connections
	#	False 	-> Bind failed
	#	True 	-> Bind succeeded
	def bind(self, host = self.host, port = self.port, backlog = self.backlog):
		self.sock = None

		# Bind to 'host' on 'port'
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((host, port))
			self.sock.listen(backlog)

		except socket.error, (value, message): #Failed
			if self.sock:
				self.sock.close()
			Logger.log("server%3d", "socket failed to bind\n\tmessage = '%s'\n\thost = '%s'\n\tport = '%s'\n\tbacklog = '%s'" % (message, host, port, backlog), visualCue = True)
			return False

		Logger.log("server%3d", "socket created\n\thost = '%s'\n\tport = '%s'\n\tbacklog = '%s'" % (host, port, backlog), visualCue = True)
		return True

	# Public method binds and starts accepting files
	#	False 	-> Start failed
	#	True 	-> Started corrctly
	def receiveFiles(receiveSize = self.receiveSize):
		# Bind
		if not self.bind():
			return False

		## Receive files ##
		while self.running:
			client, address = self.sock.accept()
			data = client.recv(receiveSize)

			if data:
				Logger.log("server%3d" % self.id, "got data\n\tdata = '%s'" % data, visualCue = True)
				client.send(data)
				Logger.log("server%3d" % self.id, "sent data to client", visualCue = True)

			client.close()
		##               ##

		self.sock.close()
		return True

	# Public method to stop accepting connections
	def stop():
		self.running = False
