import pickle #For serializing arguments over commandline
import subprocess #Running external processes
import sys #Command line arguments

class Fork:
	"""
	Fork
		Interface for forking any object with parameters (as long as it's serializable)
	"""

	def fork(newObjectr:
		"""
		fork(	newObject, # Object type
				parameters=) # dictionary of parameters to pass into newly created object
		"""

		process = subprocess.Popen(	'python ' + 'forkObject.py',
									shell=True,
									stdin=subprocess.PIPE,
									stdout=sys.stdout)
		process.stdin.write(pickle.dumps(newObject))

	fork = staticmethod(fork)

	def spawn():
		newObject = pickle.loads(sys.stdin.read())

	spawn = staticmethod(spawn)

if __name__ == "__main__":
	Fork.spawn()
