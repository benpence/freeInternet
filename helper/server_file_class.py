#!/usr/bin/python

import classMethods # Helper class
from constants import _ROOT_DIRECTORY

import serverClass

import os #Filepath

import sys #Read/write to stdio
import pickle #Serialize objects
import subprocess #Start new processes from server

_DEFAULT_PATH = ""
_JOIN_CHARACTER = "|"

class FileServer(serverClass.Server):
	"""
	FileServer(	filepath=, # location to put/look for files,
				kwargs...)


		listens on specified interfac3 (IP), port for connections
		passes successful connections to FileServerThreads

		transfer protocol client->server header is "A|B|C|" where
			A = "up" (client->server) or "down" (server->client)
			B = size of file to be transfered in bytes
				If B left blank, server sends "B|..." for filesize
			C = name of file to be transfered
			| = field delimiter 
	"""

	def __init__(self, filepath=_DEFAULT_PATH, **kwargs):
		super(FileServer, self).__init__(**kwargs)

		self.filepath = filepath

	# method called from parent to handle connection
	def createChild(self, client, id, server):
		

_FILENAME_LENGTH = 10

class FileServerChild(serverClass.ServerChild):
	"""
	FileServerChild(	client, # client socket
						id, # number unique to this process; used for logging
						server, # reference to server process; used for logging
						filepath # where files can be found/put)

		When started off from FileServer, handles file transfer
	"""

	def __init__(self, client, id, server, filepath, **kargs):
		super(FileServerChild, self).__init__(client, id, server.id, **kargs)

		self.filepath = "%s%s" % (_ROOT_DIRECTORY, filepath)
		self.state = "accepted"

	def getManifest(self):
		self.clientHost = self.client.getpeername()[0]

		data = self.client.recv(self.chunkSize)
		direction, filesize, filename, rest = data.split(_JOIN_CHARACTER)

		# Client->Server
		self.manifest = {	"direction" : direction,
							"filesize" 	: filesize,
							"file"		: os.path.join(self.filepath, filename)}

		

		return direction

	def continue(self):
		if self.state = "accepted":
			if manifest[direction] == "up":
				self.commands = { 	"openFile" 	: 'wb',
									"filesize"	: self.manifest["filesize"]),
									"transfer"	: (lambda file, bytesLeft : file.write(self.client.recv(min(bytesLeft, self.chunkSize)))}

			else:
				# Nonexistent file?
				if not os.path.exists(self.manifest["filesize"]
					self.log(	"server%03d" % self.server.id,
								"process%03d(%s) path '%s' not found for reading" % (self.id, self.clientHost, self.filepath),
									messageType = "ERR")
					return False

				self.commands = { 	"openFile" 	: 'rb',
									"filesize"	: os.path.getsize(self.manifest[file]),
									"send"		: (lambda : self.client.send(self.pad(str(self.manifest["filesize"]) + _JOIN_CHARACTER)))
									"transfer"	: (lambda file, bytesLeft : file.write(self.client.recv(min(bytesLeft, self.chunkSize)))}
				
									
			
			self.bytesLeft = int(self.manifest[filesize]) # Receive and write the bytes by chunkSize
			self.file = open(manifest[file], self.commands["openFile"]) # Open file for reading/writing

			self.state = "transferring"

			# Have to send client filesize
			if "send" in self.commands:
				self.commands["send"]()


			self.continue()

		elif self.state = "transferring":
			self.commands["transfer"].(self.file, self.bytesLeft)
			if bytesLeft < self.chunkSize:
				file.write(self.client.recv(bytesLeft))
			else:
				file.write(self.client.recv(self.chunkSize))
			bytesLeft -= self.chunkSize
			


			self.log(	"server%03d" % self.server.id,
						"process%03d(%s) received and wrote %d bytes to '%s'" % (self.id, self.clientHost, manifest[filesize], manifest[destination]))






		# Server->Client
		elif direction == "down":
			source = os.path.join(self.filepath, filename)


			# Tell client the filesize
			filesize = bytesLeft = os.path.getsize(source)

			# Transfer pieces to client
			with open(source, 'rb') as file:
				while bytesLeft > 0:
					if bytesLeft < self.chunkSize:
						self.client.send(file.read(bytesLeft))
					else:
						self.client.send(file.read(self.chunkSize))
					bytesLeft -= self.chunkSize

			self.log(	"server%03d" % self.server.id,
						"process%03d(%s) sent %d bytes of '%s' to client" % (self.id, self.clientHost, filesize, source))

		elif direction == "done":
			done = True

			self.log(	"server%03d" % self.server.id,
						"process%03d(%s) closing connection" % (self.id, self.clientHost))

		# Bad protocol
		else:
			self.log(	"server%03d" % self.server.id,
						"process%03d(%s) received bad protocol"
						"\n\tdata = '%s'" % (self.id, self.clientHost, data),
						messageType = "ERR")
			self.client.close()
			return False

		self.client.close()
		return True

if __name__ == "__main__":
	server = FileServer(filepath="./serverFiles/")
	server.listen()
