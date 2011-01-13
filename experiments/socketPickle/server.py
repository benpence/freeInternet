#!/usr/bin/python

import socket
import subprocess
import pickle

"""
A simple echo server 
"""

host = '' 
port = 50000 
backlog = 5 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog) 

while 1: 
    client, address = s.accept() 
    data = client.recv(size) 
    if data: 
        process = subprocess.Popen( 'python thread.py',
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=sys.stdout)
    process.stdin.write(pickle.dumps(client.makefile()))
    process.stdin.write(pickle.dumps(data))
