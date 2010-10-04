#!/usr/bin/python

import serverClass
import os

_DEFAULT_PATH = "./"
_JOIN_CHARACTER = "|"

class FileServer(serverClass.Server):
	"""
	FileServer(	chunkSize=, # size of data that connection will send/receive
				filepath=, # location to put/look for files
				output=, boolean, logging printed to shell?

			listens on specified interfac3 (IP), port for connections
			passes successful connections to FileServerThreads
	"""

	def __init__(self, **kwargs):
		# In case the parent/grandparent keyword arguments change,
		# kwargs will always be adequate
		if 'filepath' in kwargs:
			self.filepath = kwargs.get('filepath')
			kwargs.pop('file')
		else:
			self.filepath = _DEFAULT_PATH

		super(FileServer, self).__init__(**kwargs)

	# method called from parent to handle connection
	def createThread(self, client, data, id, server):
		thread = FileServerThread(client, data, id, server, self.filepath)
		thread.start()


_FILENAME_LENGTH = 10

class FileServerThread(serverClass.ServerThread):
	"""
	FileServerThread(	client, # client socket
						data, # data sent across socket
						id, # number unique to this thread; used for logging
						server, # reference to server process; used for logging
						filepath # where files can be found/put)

		When started off from FileServer, handles file transfer
	"""

	def __init__(self, client, data, id, server, filepath):
		super(FileServerThread, self).__init__(client, data, id, server)

		self.filepath = filepath

	def run(self):
		direction, filesize, filename = data.split(_JOIN_CHARACTER)

		# Client->Server
		if direction == "up":
			destination = os.path.join(self.filepath, filename)

			bytesLeft = filesize

			with open(destination, 'wb') as file:
				while bytesLeft > 0:
					if bytesLeft < self.chunkSize:
						file.write(self.client.recv(self.chunkSize))
						bytesLeft -= self.chunkSize
					else:
						file.write(self.client.recv(bytesLeft))
				

				self.server.log("server%03d" % self.server.id,
								"thread%03d received and wrote %d bytes to '%s'" % (self.id, self.data, destination))

		# Server->Client
		elif direction == "down":
			source = os.path.join(self.filepath, filename)

			# Nonexistent file?
			if not os.path.exists(filename):
				self.server.log("server%03d" % self.server.id,
								"thread%03d path '%s' not found for writing" % filepath,
								messageType = "ERR")
				return False

			# Tell client the filesize
			filesize = bytesLeft = os.path.getsize(source)
			self.client.send(filesize + _JOIN_CHARACTER)

			# Transfer pieces to client
			with open(source, 'rb') as file:
				while bytesLeft > 0:
					if bytesLeft < self.chunkSize:
						self.client.send(file.read(self.chunkSize))
						bytesLeft -= self.chunkSize
					else:
						self.client.send(bytesLeft)

			self.server.log("server%03d" % self.server.id,
							"thread%03d sent %d bytes of '%s' to client" % (self.id, filesize, source))

		# Bad protocol
		else:
			self.server.log("server%03d" % self.server.id,
							"thread%03d received bad protocol" % self.id
							"\n\tdata = '%s'",
							messageType = "ERR")

		self.client.close()

if __name__ == "__main__":
	server = FileServer()
	server.bind()
