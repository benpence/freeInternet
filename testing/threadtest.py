#!/usr/bin/python

"""
Threading test
"""

from threading import Thread
import time

class TestThread(Thread):
	def __init__(self, num):
		Thread.__init__(self)

		self.running = True
		self.num = num

		self.count = 0

	def run(self):
		while self.running:
			print "%d-%d" % (self.num, self.count)
			self.count += 1
			
			time.sleep(1)

if __name__ == "__main__":
	threads = []
	for i in range(10):
		hey = TestThread(i)
		hey.start()

		threads.append(hey)

		time.sleep(0.5)

	time.sleep(5)

	for thread in threads:
		thread.running = False
	
	print "DONE"

	for i in range(10000000):
		i
