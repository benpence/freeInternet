"""
Logging
"""

import datetime
import os.path

visualCues = True
logFiles = {}

def log(program, message, messageType = "log", visualCue = False):
	log = "%s\t%s\t%s:\t%s" % (datetime.datetime.now(), messageType, program, message)

	## Output to file ##
	#Open file if not already open

	if program not in logFiles:
		logFiles[program] = open("log_" + program, 'wa')

	logFiles[program].write(log + "\n")

	## Output to screen ##
	if visualCue and visualCues:
		print log

log("server", "IT DOES NOT WORK", messageType = "ERR", visualCue = True)
log("server", "ALL IS WELL", messageType = "LOG", visualCue = True)
