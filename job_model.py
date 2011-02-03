try:
    from datetime import strftime
except ImportError, e:
    from time import strftime

import model
import common

class Assign(model.Model):
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
            date_issued=strftime("%Y.%m.%d-%H:%M:%S"))

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
        
        assign.date_returned = strftime("%Y.%m.%d-%H:%M:%S")
        assign.results_path = results_path

    @classmethod
    def getNextJob(cls, ip):
        """
        ip:str -> job:Job | job_instance:int
        
        Finds next sequential job that is not assigned
        """
        
        assigns = cls.search()
        
        # First job assignment?
        if not assigns:
            return Job.search(1, id=0), 0
        
        # Already assigned something but not completed?
        already_assigned = filter(
            lambda x: x.ip == ip and x.date_returned == "",
            assigns)
        if already_assigned:
            return Job.search(1, id=already_assigned[0].id), already_assigned[0].instance
        
        # Get max job_id in Assign
        max_id = max(
            assigns,
            key=lambda x: x.id).id

        """# Don't give out multiple instances of same job to same client
        if Assign.search(1, id=max_id, ip=ip):"""
    
        # Get max job_instance
        max_assign = max(
            filter(
                lambda x: x.id == max_id,
                assigns),
            key=lambda x: x.instance)
        
        # Enough instances?
        if max_assign.instance + 1 == common._MAX_INSTANCES:
            return Job.search(1, id=max_id + 1), 0

        # More instances of same job
        return Job.search(1, id=max_id), max_assign.instance + 1        
        
        """TODO: ADD TESTS FOR WHEN THERE ARE NO MORE JOBS TO DO"""
        

class Job(model.Model):
    _keys = {
        'id' :          'INTEGER',
        }
    _values = {
        'credit' :      'INTEGER',
        'description' : 'VARCHAR',
        'complete' :    'VARCHAR',
        'job_path' :    'VARCHAR',
        }

def __setup__():
    Assign._changes = Assign._rows = {}
    Assign.writeToDatabase(common._DATABASE_PATH)
        
    for i in range(common._MAX_JOBS):
        Job(id=i,
            credit=0,
            description="TEST TEST TEST",
            job_path=common._SERVER_DIRECTORY+'/'+str(i))
    Job.writeToDatabase(common._DATABASE_PATH)

def __init__():    
    Assign.readIntoMemory(common._DATABASE_PATH)
    Job.readIntoMemory(common._DATABASE_PATH)
    Throttle.readIntoMemory(common._DATABASE_PATH)

def test():
    __init__()

    for i in range(20):
        job, job_instance = Assign.getNextJob("127.0.0.1")
        assert isinstance(job, Job)
        assert isinstance(job_instance, int)
        #print job
        for value in map(lambda x: str(x), Assign._rows.values()):
            print value
        print

        Assign.assign(job, job_instance, "127.0.0.1")
        #print Assign._rows[(0, 0)].verified

        Assign.complete("127.0.0.1", "test/TEST/test")
    
    

if __name__ == '__main__':
    test()