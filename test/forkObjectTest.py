from forkObject import Fork

class A:
	def __init__(self, test, test2=""):
		"""f = open('testing', 'w')
		f.write(test)
		f.write(test2)
		f.close()"""

		print test
		print test2

Fork.fork(A("TEST",test2="TEST2"))
