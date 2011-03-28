import os
import pickle
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
    output          = model.Field(model.String)
    verified        = model.Field(model.String)

    @classmethod    
    def complete(cls, ip, results_path):
        """
        ip:str | results_path:str -> None
        
        Mark ip's current job complete
        """
        
        assign = cls.query.get_by(
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
        return = max(
            cls.qyery.filter_by(ip=ip).all(),
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
        
        def assign(job, instance):
            # More instances of same job
            assign = q.get_by(
                id=job.id,
                instance=instance
            )

            if assign:
                assign.ip = ip
                assign.date_issued=strftime("%Y.%m.%d-%H:%M:%S")
            else:
                cls(id=job.id,
                    instance=job_instance,
                    ip=ip,
                    date_issued=strftime("%Y.%m.%d-%H:%M:%S"))
            model.commit()
            
            return pickle.loads(job.input) # in (job_name, (input_arg, ..)) format
        
        # First job assignment?
        if not q.all():
            return assign(Job.query.get_by(id=0), 0)
        
        # Already assigned something but not completed?
        already_assigned = q.get_by(
            ip=ip,
            date_returned="",
        )
        
        job_q = Job.query
        
        if already_assigned:
            job = job_q.get_by(id=first.id), first.instance
        
        # Get max job_id in Assign
        max_id = max(
            assing_q.all(),
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
                return assign(job_q.first().name, 0)
            
            # More jobs... return next sequential job, instance 0
            return assign(job_q.get_by(id=max_id + 1), 0)

class Job(model.Model):
    id              = model.Field(model.Integer, primary_key=True)
    input           = model.Field(model.String)
    description     = model.Field(model.String)
    credit          = model.Field(model.Integer)

def setup():
    import fi.job.task
    task = fi.job.task.__getattribute(TASK)__

    for i, job_input in enumerate(task.input()):
        Job(id=i,
            input=pickle.dumps(job_input),
            description=task.DESCRIPTION,
            credit=task.CREDIT
        )

        sys.out.write("%d " % i)
        sys.stdout.flush()

    model.commit()

model.mapTables()