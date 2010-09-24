#!/usr/bin/python

"""
A simple echo server
"""

import socket

host = ''
port = 50000
backlog = 5

receiveSize = 1024

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.bind((host, port))
socket.listen(backlog)

while True:
	client, address = socket.accept()
	data = client.recv(receiveSize)

	if data != 'exit':
		client.send(data)
	client.close()

