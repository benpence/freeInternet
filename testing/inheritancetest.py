#!/usr/bin/python

class A(object):
	def __init__(self, test = 3):
		print test

class myClass(A):
	def __init__(self, test = 5):
		super(myClass, self).__init__(test = test)

hey = myClass()
