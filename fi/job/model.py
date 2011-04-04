import os
import datetime
import itertools

import fi.job
import fi.model as model
from fi.throttle.model import Client # So foreign key references are valid
import fi.exception

class Job(model.Model):
    """A RemoteJob to perform"""
    id              = model.Field(model.Integer, primary_key=True, autoincrement=True)
    name            = model.Field(model.String)
    description     = model.Field(model.String)
    input_desc      = model.Field(model.String)
    output_desc     = model.Field(model.String)
    module          = model.Field(model.String, deferred=True)
    credit          = model.Field(model.Integer)
    model.using_options(order_by='id')
    
    def __repr__(self):
        return "<Job(%d,'%s')>" % (self.id, self.name)

class Instance(model.Model):
    """A RemoteJob with input to perform"""
    job             = model.ManyToOne('Job', primary_key=True)
    id              = model.Field(model.Integer, primary_key=True, autoincrement=True)
    input           = model.Field(model.PickleType)
    digest          = model.Field(model.Integer)
    model.using_options(order_by=('job_id', 'id'))
    
    def __repr__(self):
        return "<Instance(%d, %d)>" % (self.job.id, self.id)

class Assignment(model.Model):
    """A RemoteJob with input, completed by a client"""
    job             = model.ManyToOne('Job', primary_key=True)
    instance        = model.ManyToOne('Instance', primary_key=True)
    id              = model.Field(model.Integer, primary_key=True, autoincrement=True)
    client          = model.ManyToOne('Client')
    time_issued     = model.Field(model.DateTime)
    time_returned   = model.Field(model.DateTime)
    output          = model.Field(model.PickleType)
    verified        = model.Field(model.String)
    model.using_options(order_by=('job_id', 'instance_id', 'id'))
    
    def __repr__(self):
        return "<Assignment(%d, %d, %d)>" % (self.job.id, self.instance.id, self.id)
    
    old_generator = None
    
    def reset(self):
        """Reset a job for redistribution (incase it had already been done)"""
        self.client = self.time_issued = self.time_returned = self.output = None
        
    @classmethod
    def lookup(cls, ip):
        """
        ip:str -> Assignment

        Lookup up ip's latest assignment
        """
        return cls.get_by(client=Client.byIP(ip), time_returned=None)

    @classmethod
    def cycle(cls):
        """
        None -> Assignment

        When all assignments are up, this cycles through assignments 
        """
        if not cls.old_generator:
            cls.old_generator = itertools.cycle(cls.query.all())

        assignment = cls.old_generator.next()
        while assignment.time_returned == None:
            assignment = cls.old_generator.next()
        
        return assignment

    @classmethod    
    def complete(cls, ip, output):
        """
        ip:str | output:serializable -> None

        Mark ip's current job complete
        """
        assignment = cls.lookup(ip)
        
        if not assignment:
            raise fi.exception.EmptyQueryError("No assignment for completed job")

        assignment.time_returned = datetime.datetime.now()
        assignment.output = output

        model.commit()

    @classmethod
    def nextJob(cls, ip):
        """
        ip:str -> None

        Finds next sequential job that is not assigned
        Assign it to ip
        """
        # Already assigned something but not completed (this happens when the client disconnects and reconnects usually)?
        already_assigned = cls.lookup(ip)

        if already_assigned:
            return already_assigned
        
        next_job = cls.get_by(time_issued=None)

        # All complete? -> Erase last one and give it off
        if not next_job:
            redo = cls.get_by(verified="Incorrect")
            
            # Redo a failed test
            if redo:
                return redo
            
            # Pick arbitrary assignment
            return cls.cycle()

        """TODO: Don't give out multiple assignments of same job to same client. This is difficult with only 2/3 clients ;)"""
        return next_job

    @classmethod
    def record(cls, ip, assignment):
        assignment.reset()
        assignment.time_issued = datetime.datetime.now()
        assignment.client = Client.byIP(ip)
        
        model.commit()

def setup():
    """
    Reads fi/job/remote/ for jobs
    Asks ModuleNameInput class for a generator to get input
    Stores Job, then Jobs w/Input (Instance), then Jobs w/input and future output (Assignment) rows in database
    """
    prefix = os.path.join('fi', 'job', 'remote')
    files = (
        f
        for f in os.listdir(prefix)
        if  f.endswith('.py') and
            f != '__init__.py' and
            os.path.isfile(
                os.path.join(prefix, f)
            )
    )
    
    # For each RemoteJob file
    for i, filename in enumerate(files):

        name = filename.replace('.py', '')
        
        # Get input generator
        input_class = __import__('fi.job.remote.' + name).job.remote.__getattribute__(name).__getattribute__(name + "Input")
        
        # Get module code
        with open(os.path.join(prefix, filename), 'r') as module:
            module_input = module.read().split('class %sInput' % name)[0]

        # Add job
        job = Job(
            id=i,
            name=name,
            description=input_class.DESCRIPTION,
            input_desc=input_class.INPUT,
            output_desc=input_class.OUTPUT,
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