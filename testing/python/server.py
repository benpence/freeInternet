#!/usr/bin/python

"""
A simple echo server
"""

#Add helper libraries
import sys

sys.path.insert(0, "../../helper")
from logging import Logger	#Logger class

import socket

host = ''
port = 50000
backlog = 5

receiveSize = 1024

sock = None

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, port))
	sock.listen(backlog)

	Logger.log("server", "socket created\n\thost = '%s'\n\tport = '%s'\n\tbacklog = '%s'" % (host, port, backlog), visualCue = True)
except socket.error, (value, message):
	if sock:
		sock.close()

	Logger.log("server", "could not open socket '%s'" % message, visualCue = True)

while sock:
	client, address = sock.accept()
	data = client.recv(receiveSize)

	if data:
		Logger.log("server", "got data\n\tdata = '%s'" % data, visualCue = True)
		client.send(data)
		Logger.log("server", "sent data to client", visualCue = True)

	client.close()
