#!/usr/bin/python

def extract(self, keywords, kwargs):
	for keyword in keywords:
		if keyword in kwargs:
			exec "self.%s = kwargs.get('%s')" % (keyword, keyword)
			kwargs.pop(keyword)

class A(object):
	def __init__(self, hey=1, ho=2):
		self.hey = hey
		self.ho = ho

class B(A):
	def __init__(self, **kwargs):
		extract(self, ['heen'], kwargs)
		super(B, self).__init__(**kwargs)
				

test = B(hey=2, ho=3, heen=4)
print test.hey
print test.ho
print test.heen
