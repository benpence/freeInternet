import datetime

from model import Model
import common
#from throttle_model import Throttle

class Assign(Model):
    
    
    _keys = {
        'id' :          'INTEGER',
        'instance':     'INTEGER',
        }
    _values = {
        'ip' :          'VARCHAR',
        'date_issued' : 'VARCHAR',
        'date_returned':'VARCHAR',
        'results_path': 'VARCHAR',
        'verified' :    'VARCHAR',
        }

    @classmethod
    def assign(cls, job, job_instance, ip):
        """
        job:Job | job_instance:int | ip:str -> None
        
        Assign job/job_instance to ip
        """
        cls(id=job.id,
            instance=job_instance,
            ip=ip,
            date_issued=datetime.strftime("%Y.%m.%d-%H:%M:%S"))

    @classmethod    
    def complete(cls, ip, results_path):
        """
        ip:str | results_path:str -> None
        
        Mark ip's current job complete
        """
        
        assign = cls.search(
            1,
            ip=ip,
            date_returned="")
        
        if not assign:
            """ERROR: CALL AUTHORITIES"""
            return
        
        assign.date_returned = datetime.strftime("%Y.%m.%d-%H:%M:%S")
        assign.results_path = results_path

    @classmethod
    def getNextJob(cls):
        """
        None -> job:Job | job_instance:int
        
        Finds next sequential job that is not assigned
        """
        
        assigns = cls.search()
        
        # First job assignment?
        if not assigns:
            return Job.search(1, id=0), 0
        
        # Get current max job_id
        max_id = max(
            assigned,
            key=lambda x: x.id).id
        
        # ...corresponding job
        max_job = max(
            filter(
                lambda x: x.id == max_id,
                assigned),
            key=lambda x: x.instance)
        
        # Go on to next job or give out another instance?
        if max_job.instance != common._MAX_INSTANCES:
            return max_job, max_job.instance + 1
    
        """TODO: ADD TESTS FOR WHEN THERE ARE NO MORE JOBS TO DO"""
        
        return Job.search(1, id=max_job + 1)
        

class Job(Model):
    _keys = {
        'id' :          'INTEGER',
        }
    _values = {
        'credit' :      'INTEGER',
        'description' : 'VARCHAR',
        'complete' :    'VARCHAR',
        'job_path' :    'VARCHAR',
        }

def test():
    pass

def __init__():
    Assign._changes = Assign._rows = {}
    Assign.writeToDatabase(common._DATABASE_PATH)
        
    for i in range(common._MAX_JOBS):
        hey = Job(id=i,
            credit=0,
            description="TEST TEST TEST",
            job_path=common._SERVER_DIRECTORY+'/'+str(i))
    Job.writeToDatabase(common._DATABASE_PATH)
    

if __name__ == '__main__':
    test()