#!/usr/bin/python

from threading import Thread

class A(Thread):
	def __init__(self):
		Thread.__init__(self)
		
		self.hey = 5

class B(A):
	def __init__(self):
		super(B, self).__init__()

		print self.hey

hey = B()
