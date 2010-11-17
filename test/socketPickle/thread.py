#!/usr/bin/env python 

import pickle #For serializing arguments over commandline
import sys #Command line arguments
import socket 

""" 
A simple echo client 
""" 


s = pickle.loads(sys.stdin.read())
data = pickle.loads(sys.stdin.read())

s.send(data) 
s.close() 

print 'Thread received:', data
