#!/usr/bin/python

def realFunction(house, mouse, tea = 5, he = 7, truth = True):
	print "house = ", house, "\nmouse = ", mouse, "\ntea = ", tea, "\nhe = ", he, "\ntruth = ", truth

def passFunction(*args, **kargs):
	realFunction(*args, **kargs)

passFunction(1, 2, tea = 3, he = 4)
passFunction(1, 2, he = 4)
passFunction(1, 2)

def passFunction2(*args, **kargs):
	if 'he' not in kargs:
		kargs['he'] = 100
	realFunction(*args, **kargs)

passFunction2(1, 2, tea = 3)
passFunction2(1, 2, tea = 3, he = 4)

class A(object):
	X = 50
	def __init__(self, thing = X):
		print thing

A()
