#!/usr/bin/python

#Add helper libraries
import sys

sys.path.insert(0, "../helper")
from constants import _ROOT_DIRECTORY #Root directory
from logging import Logger	#Logger class
import fileClientClass #FileClient class

import subprocess #Running external processes

_DEFAULT_JOB_DIRECTORY = "%sclient/test/" % _ROOT_DIRECTORY

class ClientApplication:

	def __init__(self, jobDirectory=_DEFAULT_JOB_DIRECTORY):
		self.jobDirectory = jobDirectory

		client = fileClientClass.FileClient(filepath="client/test/", output=True)

		client.enqueueTransfer("down", "job.tar.gz")
		client.connect()

		self.doJob()

		client.enqueueTransfer("up", "results.tar.gz")
		client.connect()

	def doJob(self):
		process = subprocess.Popen(	'tar xvf %sjob.tar.gz -C %s' % (self.jobDirectory, self.jobDirectory),
									shell=True,
									stdout=subprocess.PIPE)

		process = subprocess.Popen(	'%sdoJob < %sjobInput' % (self.jobDirectory, self.jobDirectory),
									shell=True,
									stdin=open('%sjobInput' % self.jobDirectory, 'r'),
									stdout=subprocess.PIPE)
		open('%sjobOutput' % self.jobDirectory, 'w').write(process.stdout.read())

		process = subprocess.Popen(	'tar cvzf %sresults.tar.gz -C %s jobOutput' % (self.jobDirectory, self.jobDirectory),
									shell=True)

		#subprocess.Popen('rm %sjobInput %sdoJob', shell=True)
	def log(self, *args, **kargs):
		if 'output' not in kargs:
			kargs['output'] = self.output

		logging.Logger.log(*args, **kargs)


def Main():
	app = ClientApplication()

if __name__ == "__main__":
	Main()
