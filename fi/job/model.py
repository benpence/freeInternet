import os
import datetime
import itertools

import fi.job
import fi.model as model
from fi.throttle.model import Client # So foreign key references are valid
import fi.exception as exception

class Job(model.Model):
    id              = model.Field(model.Integer, primary_key=True, autoincrement=True)
    name            = model.Field(model.String)
    description     = model.Field(model.String)
    module          = model.Field(model.String, deferred=True)
    credit          = model.Field(model.Integer)

class Instance(model.Model):
    job             = model.ManyToOne('Job', primary_key=True)
    id              = model.Field(model.Integer, primary_key=True, autoincrement=True)
    input           = model.Field(model.PickleType)
    digest          = model.Field(model.Integer)

class Assignment(model.Model):
    job             = model.ManyToOne('Job', primary_key=True)
    instance        = model.ManyToOne('Instance', primary_key=True)
    id              = model.Field(model.Integer, primary_key=True, autoincrement=True)
    client          = model.ManyToOne('Client')
    date_issued     = model.Field(model.DateTime)
    date_returned   = model.Field(model.DateTime)
    output          = model.Field(model.PickleType)
    verified        = model.Field(model.String)
    
    old_generator = None
    
    def reset(self):
        self.client = self.date_issued = self.date_returned = self.output = None
        
    @classmethod
    def asc(cls):
        return cls.query.order_by(model.asc(cls.job))

    @classmethod
    def lookup(cls, ip):
        """
        ip:str -> Assignment

        Lookup up ip's latest assignment
        """
        return cls.get_by(client=Client.byIP(ip), date_returned=None)

    @classmethod
    def cycle(cls):
        """
        None -> Assignment

        When all assignments are up, this cycles through assignments 
        """
        if not cls.old_generator:
            cls.old_generator = itertools.cycle(cls.query.all())

        assignment = cls.old_generator.next()
        while assignment.date_returned == None:
            assignment = cls.old_generator.next()
        
        return assignment

    @classmethod    
    def complete(cls, ip, output):
        """
        ip:str | output:_ -> None

        Mark ip's current job complete
        """
        assignment = cls.lookup(ip)

        if not assignment:
            raise exception.EmptyQueryError("No assignment for completed job")

        assignment.date_returned = datetime.datetime.now()
        assignment.output = output

        model.commit()

    @classmethod
    def getNextJob(cls, ip):
        """
        ip:str -> None

        Finds next sequential job that is not assigned
        Assign it to ip
        """
        # Already assigned something but not completed?
        already_assigned = cls.lookup(ip)

        if already_assigned:
            job = Job.get_by(id=first.id)
            
        next_job = cls.asc().filter_by(date_issued=None).first()

        # All complete? -> Erase last one and give it off
        if not next_job:
            redo = cls.get_by(verified="Incorrect")
            
            # Redo a failed test
            if redo:
                return redo
            
            # Pick arbitrary assignment
            return cls.cycle()

        """TODO: Don't give out multiple instances of same job to same client"""
        return next_job

    @classmethod
    def record(cls, ip, assignment):
        assignment.reset()
        assignment.date_issued = datetime.datetime.now()
        assignment.client = Client.byIP(ip)
        
        model.commit()

def nameToInput(task_name):
    return __import__('fi.job.remote.' + task_name).job.remote.__getattribute__(task_name).__getattribute__(task_name + "Input")

def setup():
    prefix = os.path.join('fi', 'job', 'remote')
    
    for i, filename in enumerate(os.listdir(prefix)):
        if not filename.endswith('.py') or filename == '__init__.py':
            continue
        
        # Add job
        name = filename.replace('.py', '')
        input_class = nameToInput(name)
        
        with open(os.path.join(prefix, filename), 'r') as module:
            module_input = module.read().split('class %sInput' % name)[0]
        
    
        job = Job(
            id=i,
            name=name,
            description=input_class.DESCRIPTION,
            module=module_input,
            credit=input_class.CREDIT
        )
    
        # Add instances
        for j, instance_input in enumerate(input_class.input(fi.job.MAX_INSTANCES)):
            instance = Instance(
                id=j,
                job=job,
                input=instance_input,
            )

            # Add assignments
            for k in range(fi.job.MAX_ASSIGNMENTS):
                Assignment(
                    id=k,
                    job=job,
                    instance=instance,
                )
    
    model.commit()

model.mapTables()