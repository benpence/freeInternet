#!/usr/bin/python

"""
Client - class for connecting on a port for connection
"""

import sys

sys.path.insert(0, "../helper")
from logging import Logger	#Logger class

import socket

class Client:
	clients = {}
	count = 0

	def __init__(self, host = 'localhost', port = 5556, receiveSize = 1024):
		self.host = host
		self.port = port

		self.id = self.count			#client identifier for logging
		Client.count += 1				
		Client.clients[self.id] = self	#singelton

	# Set up connection to server
	#	False 	-> Connection failed
	#	True 	-> Connection succeeded
	def connect(self, host = self.host, port = self.port):
		self.sock = None

		# Connect to server
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((host, port))

		except socket.error, (value, message): #Failed
			if self.sock:
				self.sock.close()

			Logger.log("client%3d", "failed to connect\n\tmessage = '%s'\n\thost = '%s'\n\tport = '%s'" % (message, host, port), visualCue = True)
			return False

		Logger.log("client%3d", "socket connected\n\thost = '%s'\n\tport = '%s'" % (host, port), visualCue = True)
		return True
	
	# Public method allows sending of files
	#	False 	-> File send faild
	#	True 	-> File send succeeded
	def sendFile(filename, path = None, host = self.host, port = self.port):
		# Connect
		if not self.connect(host = host, port = port):
			return False #Not connected properly

		## Send file ##
		sock.send('Hello, world')
		data = sock.recv(receiveSize)

		Logger.log("client%3d", "sent '%s', received '%s'" % ('Hello, world', data))
		##           ##

		# Disconnect
		self.sock.close()
