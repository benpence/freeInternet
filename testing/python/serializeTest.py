#!/usr/bin/python

import pickle #For serializing arguments over commandline
import subprocess #Running external processes
import sys #Command line arguments

class Test:
	def __init__(self, printout, now):
		print printout, now

def spawn(format, fields):
	# Tell receiver how many items
	process = subprocess.Popen(	'python serializeTest.py %s' % format,
								shell=True,
								stdin=subprocess.PIPE,
								stdout=sys.stdout)
	process.stdin.write(pickle.dumps(fields))

if __name__ == "__main__":
	#Spawned thread?
	if len(sys.argv) is 2:
		format = sys.argv[1]
		fields = pickle.loads(sys.stdin.read())

		thing = format + "(" + ','.join(fields) + ")"
		print thing

		eval(thing)

	#Starting thread
	else:
		spawn("Test", ["\"PRINT THIS SHIT OUT\"", "\"NOW\""])
