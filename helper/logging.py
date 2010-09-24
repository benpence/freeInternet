"""
Logging
"""


import datetime
import os.path

visualCues = True

logFiles = {}

def log(program, messageType = "log", message, visualCue = False):
	log = "%s\t%s\t%s\t%s:\t%s\n" % (datetime.datetime.now(), messageType, program, message)

	## Output to file ##
	#Open file if not already open

	if program not in files:
		logFiles[program] = open("log_" + program, 'w')

	logFiles[program].write(log)

	## Output to screen ##
	if visualCue and visualCues:
		print log
