#!/usr/bin/python

"""
Logging
"""

import datetime
import os.path

class Logger:
	logFiles = {}
	visualCues = True

	def log(program, message, messageType = "LOG", visualCue = False):
		log = "%s\t%s\t%s:\t%s" % (datetime.datetime.now(), messageType, program, message)

		## Output to file ##
		#Open file if not already open

		if program not in Logger.logFiles:
			Logger.logFiles[program] = open("log_" + program, 'wa')

		Logger.logFiles[program].write(log + "\n")

		## Output to screen ##
		if visualCue and Logger.visualCues:
			print log

	log = staticmethod(log)

	def __close__():
		for file in Logger.logFiles:
			file.close()

if __name__ == "__main__":
	test = Logger()

	test.log("server", "IT DOES NOT WORK", messageType = "ERR", visualCue = True)
	test.log("server", "ALL IS WELL", messageType = "LOG", visualCue = True)
