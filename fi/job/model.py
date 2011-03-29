import os
try:
    from datetime import strftime
except ImportError, e:
    from time import strftime

import fi.job
import fi.model as model
import fi.exception as exception

class Assign(model.Model):
    id              = model.Field(model.Integer, primary_key=True)
    instance        = model.Field(model.Integer, primary_key=True)
    ip              = model.Field(model.String)
    date_issued     = model.Field(model.String)
    date_returned   = model.Field(model.String)
    output          = model.Field(model.PickleType)
    verified        = model.Field(model.String)

    @classmethod    
    def complete(cls, ip, results_path):
        """
        ip:str | results_path:str -> None
        
        Mark ip's current job complete
        """
        assign = cls.get_by(
            ip=ip,
            date_returned=""
        )
        
        if not assign:
            raise exception.EmptyQueryError("No assignment for completed job")
        
        assign.date_returned = strftime("%Y.%m.%d-%H:%M:%S")
        assign.results_path = results_path
        
        model.commit()

    @classmethod
    def lookup(cls, ip):
        """
        ip:str -> Assign
                
        Lookup up ip's latest assignment
        """
        return max(
            cls.query.filter_by(ip=ip).all(),
            key=lambda x: int("%d%d" % (x.id, x.instance))
        )

    @classmethod
    def getNextJob(cls, ip):
        """
        ip:str -> None
        
        Finds next sequential job that is not assigned
        Assign it to ip
        """
        q = cls.query

        def record(job, instance):
            # More instances of same job
            assign = cls.get_by(
                id=job.id,
                instance=instance
            )

            if assign:
                assign.ip = ip
                assign.date_issued=strftime("%Y.%m.%d-%H:%M:%S")
            else:
                cls(id=job.id,
                    instance=instance,
                    ip=ip,
                    date_issued=strftime("%Y.%m.%d-%H:%M:%S"))
            model.commit()
            
            return job # in (job_name, (input_arg, ..)) format
        
        # First job assignment?
        if not q.all():
            return record(Job.get_by(id=0), 0)
        
        # Already assigned something but not completed?
        already_assigned = cls.get_by(
            ip=ip,
            date_returned="",
        )
        
        if already_assigned:
            job = Job.get_by(id=first.id), first.instance
        
        # Get max job_id in Assign
        max_id = max(
            q.all(),
            key=lambda x: x.id
        ).id

        """TODO: Don't give out multiple instances of same job to same client
        if Assign.search(1, id=max_id, ip=ip):"""
    
        # Get max job_instance
        max_instance = max(
            q.filter_by(id=max_id).all(),
            key=lambda x: x.instance
        ).instance
        
        # Enough instances?
        if max_instance + 1 == fi.job.MAX_INSTANCES:
            # All jobs complete?
            if max_id + 1 == fi.job.MAX_JOBS:
                return record(Job.query.first().name, 0)
            
            # More jobs... return next sequential job, instance 0
            return record(Job.get_by(id=max_id + 1), 0)

class Job(model.Model):
    id              = model.Field(model.Integer, primary_key=True)
    input           = model.Field(model.PickleType)
    description     = model.Field(model.String)
    credit          = model.Field(model.Integer)

def nameToJob(task_name):
    return __import__('fi.job.task.' + task_name).job.task.__getattribute__(task_name).__getattribute__(task_name)

def setup():
    task = nameToJob(fi.job.TASK)

    for i, job_input in enumerate(task.input(fi.job.MAX_JOBS)):
        Job(id=i,
            input=job_input,
            description=task.DESCRIPTION,
            credit=task.CREDIT
        )
        
    model.commit()
    
model.mapTables()