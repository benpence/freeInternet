#!/usr/bin/python

"""
Logging
"""

import datetime
import os.path

class Logger:
	logFiles = {}
	visualCues = True

	# Writes message to respective log file
	def log(program, message, messageType = "LOG", visualCue = False):
		log = "%s %s %s: %s" % (datetime.datetime.now(), messageType, program, message)

		## Output to file ##
		#Open file if not already open
		if program not in Logger.logFiles:
			Logger.logFiles[program] = open("log_" + program, 'wa')

		Logger.logFiles[program].write(log + "\n")

		## Output to screen ##
		if visualCue and Logger.visualCues:
			print log
	log = staticmethod(log)

	def close():
		for file in Logger.logFiles:
			file.close()
	close = staticmethod(close)
	
# Test
if __name__ == "__main__":
	Logger.log("logger", "testing error", messageType = "ERR", visualCue = True)
	Logger.log("logger", "testing log", messageType = "LOG", visualCue = True)
