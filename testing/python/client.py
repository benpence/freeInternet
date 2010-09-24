#!/usr/bin/python

"""
A simple echo client
"""

import socket

host = 'localhost'
port = 50000

receiveSize = 1024

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((host, port))
socket.send('Hello, world')

data = socket.recv(receiveSize)

socket.close()

print 'Received:', data
