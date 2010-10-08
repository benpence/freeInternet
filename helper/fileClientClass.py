#!/usr/bin/python

import clientClass
import os

_DEFAULT_PATH = ""
_JOIN_CHARACTER = "|"

class FileClient(clientClass.Client):
	"""
	FileClient(	filepath=, # location to put/look for files,
				kwargs...)

		Enqueue files to be send/received with enqueueTransfer()
		Start transfer by calling connect()

		transfer protocol client->server header is "A|B|C|..." where
			A = "up" (client->server) or "down" (server->client)
			B = size of file to be transfered in bytes
				If B left blank, server sends "B|..." for filesize
			C = name of file to be transfered
			| = field delimiter 

			when done, send "done|||..."
	"""

	def __init__(self, filepath=_DEFAULT_PATH, **kwargs):
		super(FileClient, self).__init__(**kwargs)

		self.filepath = filepath
		self.fileQueue = []

	def connectActions(self):
		for transfer in self.fileQueue:
			direction, filename = transfer

			# Client->Server
			if direction == "up":
				source = os.path.join(self.filepath, filename)

				# Nonexistent file?
				if not os.path.exists(source):
					self.log(	"client%03d" % self.client.id,
								"file to send not found"
								"\n\tdirection = '%s'"
								"\n\tsource = '%s'" % (direction, source))
					return False

				filesize = bytesLeft = os.path.getsize(source)

				# Send header
				header = _JOIN_CHARACTER.join([	direction,
												str(os.path.getsize(source)),
												filename,
												""])
				self.sock.send(self.pad(header))

				# Transfer pieces to server
				with open(source, 'rb') as file:
					while bytesLeft > 0:
						if bytesLeft < self.chunkSize:
							self.sock.send(file.read(bytesLeft))
						else:
							self.sock.send(file.read(self.chunkSize))
						bytesLeft -= self.chunkSize

				self.log(	"client%03d" % self.id,
							"sent %d bytes of '%s' to server" % (filesize, source))

			# Server->Client
			elif direction == "down":
				destination = os.path.join(self.filepath, filename)

				# Send header
				header = _JOIN_CHARACTER.join([	direction,
												"",
												filename,
												""])
				self.sock.send(self.pad(header))

				# Receive filesize
				data = self.sock.recv(self.chunkSize)
				filesize = bytesLeft = int(data.split(_JOIN_CHARACTER)[0])

				# Receive file chunks
				with open(destination, 'wb') as file:
					while bytesLeft > 0:
						if bytesLeft < self.chunkSize:
							file.write(self.sock.recv(bytesLeft))
						else:
							file.write(self.sock.recv(self.chunkSize))
						bytesLeft -= self.chunkSize

				self.log(	"client%03d" % self.id,
							"received %d into file '%s'" % (filesize, destination))
			else:
				self.log(	"client%03d" % self.id,
							"bad protocol"
							"\n\tdirection = '%s'"
							"\n\tfilename = '%s'" % (direction, filename),
							messageType = "ERR")

				return False

		header = _JOIN_CHARACTER.join(["done", "", "", ""])
		self.sock.send(self.pad(header))

		self.fileQueue = []

		return True

	def enqueueTransfer(self, direction, filename):
		"""
			enqueueTransfer(direction, # "up" means ->Server, "down" means ->Client
							filename)
		"""
		self.fileQueue.append((direction, filename))

if __name__ == "__main__":
	client = FileClient(output=True, filepath="./clientFiles/")
	client.enqueueTransfer("down", "test")
	client.connect()
