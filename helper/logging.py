#!/usr/bin/python

"""
Logging
"""

import datetime
import os.path

class Logger:
	def __init__(self):
		self.visualCues = True
		self.logFiles = {}

	def log(self, program, message, messageType = "log", visualCue = False):
		log = "%s\t%s\t%s:\t%s" % (datetime.datetime.now(), messageType, program, message)

		## Output to file ##
		#Open file if not already open

		if program not in self.logFiles:
			self.logFiles[program] = open("log_" + program, 'wa')

		self.logFiles[program].write(log + "\n")

		## Output to screen ##
		if visualCue and self.visualCues:
			print log


if __name__ == "__main__":
	test = Logger()

	test.log("server", "IT DOES NOT WORK", messageType = "ERR", visualCue = True)
	test.log("server", "ALL IS WELL", messageType = "LOG", visualCue = True)
