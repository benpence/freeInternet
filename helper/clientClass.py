#!/usr/bin/python

"""
Client - connect to a server and send files; look at 'main' function for usage
"""

from connectionClass import Connection
import socket

class Client(Connection):
	DEFAULT_HOST = 'localhost'
	DEFAULT_PORT = 5555

	def __init__(self, **kwargs):
		super(Client, self).__init__(self, **kwargs)

		self.queue = []

	# Set up connection to server
	#	False 	-> Connection failed
	#	True 	-> Connection succeeded
	def connect(self, host = DEFAULT_HOST, port = DEFAULT_PORT):
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

			self.log("client%3d" % self.id, "failed to connect\n\tmessage = '%s'\n\thost = '%s'\n\tport = '%s'" % (message, host, port), messageType = "ERR")
			return False

		self.log("client%3d" % self.id, "socket connected\n\thost = '%s'\n\tport = '%s'" % (host, port))
		return True

	def sendFile(self, filepath):
		self.queue.append(filepath)

	def sendFileFromQueue(self, filepath):
		self.sock.send(filepath)
		data = self.sock.recv(self.chunkSize)

		self.log("client%3d" % self.id, "\n\tsent '%s\n\treceived '%s'" % (filepath, data))
		return True
	
	def run(self):
		while self.running:
			if len(self.queue) > 0 and self.sock:

				# Returns true on successful send, otherwise try send again
				if self.sendFileFromQueue(self.queue[0]):
					self.queue.pop(0)

		self.sock.close()
		self.sock = None

	def close(self):
		self.running = False

if __name__ == "__main__":
	cli = Client()
	cli.connect()
	cli.sendFile("Hello, world")
	cli.start()
