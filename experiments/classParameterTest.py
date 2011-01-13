#!/usr/bin/python

class A:
	def __init__(self, classType):
		hey = classType(3)

class B:
	def __init__(self, number):
		print number**number

hey = A(B)
