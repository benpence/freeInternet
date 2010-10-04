#!/usr/bin/python

import clientClass
import os

_DEFAULT_PATH = "./"
_JOIN_CHARACTER = "|"

class FileClient(clientClass.Client):
	"""
	FileClient(	chunkSize=, # size of data that connection will send/receive
				filepath=, # location to put/look for files
				output=, # boolean, logging printed to shell?

		Enqueue files to be send/received with enqueueTransfer()
		Start transfer by calling connect()
	"""

	def __init__(self, **kwargs):
		# In case the parent/grandparent keyword arguments change,
		# kwargs will always be adequate
		if 'filepath' in kwargs:
			self.filepath = kwargs.get('filepath')
			kwargs.pop('file')
		else:
			self.filepath = _DEFAULT_PATH

		super(FileClient, self).__init__(**kwargs)

		self.fileQueue = []

	# 
	def connectActions(self):
		for transfer in self.fileQueue:
			direction, filename = transfer

			# Client->Server
			if direction == "up" and os.path.file:
				source = os.path.join(self.filepath, filename)

				# Nonexistent file?
				if not os.path.exists(source):
					self.log(	"client%03d" % self.client.id,
								"file to send not found"
								"\n\tdirection = '%s'" % direction
								"\n\tsource = '%s'" % source)
					return False

				filesize = os.path.getsize(source)

				header = _JOIN_CHARACTER.join([	direction,
												os.path.getsize(source),
												filename])
				self.sock.send(header)

				# Split into pieces
				fullChunks = filesize / self.chunkSize
				lastChunk = filesize % self.chunkSize

				# Transfer pieces to client
				with open(source, 'rb') as file:
					while fullChunks > 0:
						self.sock.send(file.read(self.chunkSize))

						fullChunks -= 1
					if lastChunk != 0:
						self.sock.send(file.read())

				self.server.log("client%03d" % self.id,
								"sent %d bytes of '%s' to server" % (filesize, source))

			# Server->Client
			elif direction == "down":
				destination = os.path.join(self.filepath, filename)

				# Tell server which file you want
				header = _JOIN_CHARACTER.join([	direction,
												"",
												filename])
				self.sock.send(header)

				# Receive filesize
				data = self.sock.recv(self.chunkSize)
				filesize = bytesLeft = data.split(_JOIN_CHARACTER)[0]

				# Receive file chunks
				with open(destination, 'wb') as file:
					while bytesLeft > 0:
						# End case
						if bytesLeft < self.chunkSize:
							file.write(self.sock.recv(bytesLeft))
							bytesLeft -= self.chunkSize
						else:
							file.write(self.sock.recv(self.chunkSize))

				self.log(	"client%03d" % self.id,
							"received %d into file '%s'" % (filesize, destination))
			else:
				self.log(	"client%03d" % self.id,
							"bad protocol"
							"\n\tdirection = '%s'" % direction
							"\n\tfilename = '%s'" % filename

	def enqueueTransfer(self, direction, filename):
		"""
			enqueueTransfer(direction, # "up" means ->Server, "down" means ->Client
							filename)
		"""
		self.fileQueue.append((direction, filename))
