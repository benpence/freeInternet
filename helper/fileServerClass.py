#!/usr/bin/python

import serverClass
import os

_DEFAULT_PATH = ""
_JOIN_CHARACTER = "|"

class FileServer(serverClass.Server):
	"""
	FileServer(	chunkSize=, # size of data that connection will send/receive
				filepath=, # location to put/look for files
				output=, boolean, logging printed to shell?

		listens on specified interfac3 (IP), port for connections
		passes successful connections to FileServerThreads

		transfer protocol client->server header is "A|B|C|" where
			A = "up" (client->server) or "down" (server->client)
			B = size of file to be transfered in bytes
				If B left blank, server sends "B|..." for filesize
			C = name of file to be transfered
			| = field delimiter 
	"""

	def __init__(self, **kwargs):
		# In case the parent/grandparent keyword arguments change,
		# kwargs will always be adequate
		if 'filepath' in kwargs:
			self.filepath = kwargs.get('filepath')
			kwargs.pop('filepath')
		else:
			self.filepath = _DEFAULT_PATH

		super(FileServer, self).__init__(**kwargs)

	# method called from parent to handle connection
	def createThread(self, client, id, server):
		thread = FileServerThread(client, id, server, self.filepath)
		thread.start()


_FILENAME_LENGTH = 10

class FileServerThread(serverClass.ServerThread):
	"""
	FileServerThread(	client, # client socket
						id, # number unique to this thread; used for logging
						server, # reference to server process; used for logging
						filepath # where files can be found/put)

		When started off from FileServer, handles file transfer
	"""

	def __init__(self, client, id, server, filepath):
		super(FileServerThread, self).__init__(client, id, server)

		self.filepath = filepath

	def run(self):
		done = False

		clientHost = self.client.getpeername()[0]
		while not done:
			data = self.client.recv(self.server.chunkSize)
			direction, filesize, filename, rest = data.split(_JOIN_CHARACTER)

			# Client->Server
			if direction == "up":
				destination = os.path.join(self.filepath, filename)

				bytesLeft = filesize = int(filesize)

				# Receive and write the bytes by chunkSize
				with open(destination, 'wb') as file:
					while bytesLeft > 0:
						if bytesLeft < self.server.chunkSize:
							file.write(self.client.recv(bytesLeft))
						else:
							file.write(self.client.recv(self.server.chunkSize))
						bytesLeft -= self.server.chunkSize

					self.server.log("server%03d" % self.server.id,
									"thread%03d(%s) received and wrote %d bytes to '%s'" % (self.id, clientHost, filesize, destination))

			# Server->Client
			elif direction == "down":
				source = os.path.join(self.filepath, filename)

				# Nonexistent file?
				if not os.path.exists(source):
					self.server.log("server%03d" % self.server.id,
									"thread%03d(%s) path '%s' not found for reading" % (self.id, clientHost, self.filepath),
									messageType = "ERR")
					return False

				# Tell client the filesize
				filesize = bytesLeft = os.path.getsize(source)
				self.client.send(self.server.pad(str(filesize) + _JOIN_CHARACTER))

				# Transfer pieces to client
				with open(source, 'rb') as file:
					while bytesLeft > 0:
						if bytesLeft < self.server.chunkSize:
							self.client.send(file.read(bytesLeft))
						else:
							self.client.send(file.read(self.server.chunkSize))
						bytesLeft -= self.server.chunkSize

				self.server.log("server%03d" % self.server.id,
								"thread%03d(%s) sent %d bytes of '%s' to client" % (self.id, clientHost, filesize, source))

			elif direction == "done":
				done = True

				self.server.log("server%03d" % self.server.id,
								"thread%03d(%s) closing connection" % (self.id, clientHost))

			# Bad protocol
			else:
				self.server.log("server%03d" % self.server.id,
								"thread%03d(%s) received bad protocol"
								"\n\tdata = '%s'" % (self.id, clientHost, data),
								messageType = "ERR")
				self.client.close()
				return False

		self.client.close()
		return True

if __name__ == "__main__":
	server = FileServer(filepath="./serverFiles/")
	server.listen()
