#!/usr/bin/python

"""
A simple echo client
"""

import socket
import sys

sys.path.insert(0, "../../helper")
from logging import Logger	#Logger class

host = 'localhost'
port = 50000
receiveSize = 1024

sock = None

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, port))

	Logger.log("client", "socket connected\n\thost = '%s'\n\tport = '%s'" % (host, port), visualCue = True)
except socket.error, (value, message):
	if sock:
		sock.close()

	Logger.log("client", "failed to connect\n\thost = '%s'\n\tport = '%s'" % (host, port), visualCue = True)
	sys.exit(1)

sock.send('Hello, world')
data = sock.recv(receiveSize)

Logger.log("client", "sent '%s', received '%s'" % ('Hello, world', data))

sock.close()
