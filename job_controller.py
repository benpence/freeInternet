"""
job_controller.py

"""

from job_model import JobModel

class Controller(object):
	pass

class JobModelServerController(Controller):
	
	@classmethod
	def getNextJobl(cls, client):
		"""
		Client -> JobModel
		
		"""
		
		if JobModelServerControler.isAssigned(client):
			return JobModel.getJobModel(client)
		
		job = JobModel.getNextJobModel()
		JobModel.assign(client, job)
		return 
	
	@classmethod
	def verifyJob(cls, client):
		"""
		Client -> Bool
		"""
		
		return verified
	
	@classmethod	
	def lookupJob(cls, client):
		"""
		Client -> JobModel
		"""
		
		return job
	
	@classmethod	
	def isAssigned(cls, client):
		"""
		Client -> Bool
		"""
		
		return lookupJobModel(client) is None
	
class JobClientController(Controller):
	pass
	
	
def test():
	pass


if __name__ == '__main__':
	test()

