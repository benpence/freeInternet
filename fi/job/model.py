import os
try:
    from datetime import strftime
except ImportError, e:
    from time import strftime

import fi
import fi.job
import fi.model as model
import fi.exception as exception

from fi.throttle.model import Throttle

class Assign(model.Model):
    id              = model.Field(model.Integer, primary_key=True)
    instance        = model.Field(model.Integer, primary_key=True)
    ip              = model.Field(model.String)
    date_issued     = model.Field(model.String)
    date_returned   = model.Field(model.String)
    results_path    = model.Field(model.String)
    verified        = model.Field(model.String)

    @classmethod
    def assign(cls, job, job_instance, ip):
        """
        job:Job | job_instance:int | ip:str -> None
        
        Assign job/job_instance to ip
        """
        assign = cls.query.filter_by(
            id=job.id,
            instance=job_instance
        ).one()

        if assign:
            assign.ip = ip
            assign.date_issued=strftime("%Y.%m.%d-%H:%M:%S")
        else:
            cls(id=job.id,
                instance=job_instance,
                ip=ip,
                date_issued=strftime("%Y.%m.%d-%H:%M:%S"))
        
        model.commit()

    @classmethod    
    def complete(cls, ip, results_path):
        """
        ip:str | results_path:str -> None
        
        Mark ip's current job complete
        """
        
        assign = cls.query.filter_by(
            ip=ip,
            date_returned=""
        ).first()
        
        if not assign:
            raise exception.EmptyQueryError("No assignment for completed job")
        
        assign.date_returned = strftime("%Y.%m.%d-%H:%M:%S")
        assign.results_path = results_path
        
        model.commit()

    @classmethod
    def getNextJob(cls, ip):
        """
        ip:str -> job:Job | job_instance:int
        
        Finds next sequential job that is not assigned
        """
        
        assigns = cls.query.all()
        
        # First job assignment?
        if not assigns:
            return Job.search(1, id=0), 0
        
        # Already assigned something but not completed?
        already_assigned = filter(
            lambda x: x.ip == ip and x.date_returned == "",
            assigns
        )
        if already_assigned:
            first = already_assigned[0]
            return Job.query.filter_by(id=first.id).one(), first.instance
        
        # Get max job_id in Assign
        max_id = max(
            assigns,
            key=lambda x: x.id
        ).id

        """TODO: Don't give out multiple instances of same job to same client
        if Assign.search(1, id=max_id, ip=ip):"""
    
        # Get max job_instance
        max_instance = max(
            filter(
                lambda x: x.id == max_id,
                assigns
            ),
            key=lambda x: x.instance
        ).instance
        
        # Enough instances?
        if max_instance + 1 == fi.job.MAX_INSTANCES:
            # All jobs complete?
            if max_id + 1 == fi.job.MAX_JOBS:
                return Job.query.first()(1), 0
            
            # More jobs... return next sequential job, instance 0
            return Job.search(1, id=max_id + 1), 0

        # More instances of same job
        return Job.search(1, id=max_id), max_instance + 1

class Job(model.Model):
    id              = model.Field(model.Integer, primary_key=True)
    credit          = model.Field(model.Integer)
    description     = model.Field(model.String)
    complete        = model.Field(model.String)
    job_path        = model.Field(model.String)

def __setup__(generator, description):
    Assign._changes = Assign._rows = {}
    Assign.writeToDatabase(fi.DATABASE_PATH)
    
    task_module = __import__(
        '.'.join(fi.job.TASK_DIRECTORY + [fi.job.TASK])
    )
    binary_path = os.pat h.join(fi.job.TASK_DIRECTORY)
        
    for i in task_module.input(fi.job.MAX_JOBS, ):
        Job(id=i,
            credit=5,
            description="TEST TEST TEST",
            job_path=fi.job.JOBS_DIRECTORY+'/'+str(i)
        )
    Job.writeToDatabase(fi.DATABASE_PATH)

def __init__():    
    Assign.readIntoMemory(fi.DATABASE_PATH)
    Job.readIntoMemory(fi.DATABASE_PATH)
    Throttle.readIntoMemory(fi.DATABASE_PATH)