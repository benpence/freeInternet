import itertools
import hashlib

import fi.job
import fi.model as model
from fi.job.model import Assign, Job
from fi.throttle.model import Throttle

class Verifier(object):
    @classmethod
    def init(cls):
        """
        None -> None
        
        """
        cls.verifications = {}
        
        for assign in Assign.query.filter_by(verified="").all():
            # Don't want incomplete jobs
            if assign.date_returned != "":
                cls.verify(assign)
    
    @classmethod
    def verify(cls, assign):
        """
        assign:Assign -> None
        
        """
    
        print "Verifying %d-%d" % (id, instance)
        
        m = hashlib.md5()        
        m.update(assign.output)
        cls._storeHash(assign, m.digest())
    
    @classmethod
    def _storeHash(cls, assign, digest):
        """
        assign:Assign | digest:str -> None
        
        """

        if assign.id not in cls.verifications:
            cls.verifications[assign.id] = (
                assign.instance,
                digest
            )
        else:
            cls.verifications[assign.id].append((
                assign.instance,
                digest
            ))
        
        # Time to validate?
        if len(cls.verifications[assign.id]) == fi.job.MAX_INSTANCES:
            cls._verifyResults(assign.id)
    
    @classmethod
    def _verifyResults(cls, id):
        """
        id:int -> None
        
        Called when all job instances have been completed.
        
        Is a hash is favored over the others?
        Yes -> "Passed" to majority, "Failed for rest"
        No  -> "Inconclusive" for all
        """
        
        results = cls.verifications[id]
        digests = {}
        
        for (instance, digest) in results:
            if digest not in digests:
                digests[digest] = [instance]
            else:
                digests[digest].append(instance)
                 
        majority_digest = max(
            digests.values(),
            key=lambda x : len(x))
        
        # False majority? = other > majority
        false_majority = len(
            filter(
                lambda x: x != majority_digest and len(x) >= len(majority_digest),
                digests.values()
            )
        )
        
        if not false_majority:
            # Majority md5 pass
            cls._setVerified([majority_digest], id, "Passed")
            
            # All others fail
            cls._setVerified(
                (ids
                 for ids in digests.values()
                 if ids != majority_digest
                ),
                id,
                "Failed"
            )
            
        else:
            # More than one 'max' -> inconclusive
            cls._setVerified(digests.values(), "Inconclusive")

        del cls.verifications[id]
        model.commit()
    
    @classmethod        
    def _setVerified(cls, digests, id, conclusion):
        """
        digests:[[int]] | id:int | conclusion:str -> None
        
        """
        for instance in itertools.chain(*digests):
            assign = Assign.query.filter_by(id=id, instance=instance).one()
            assign.verified = conclusion
            
            if conclusion == "Passed":
                credit = Job.query.filter_by(id=id).one().credit
                
                client = Throttle.query.filter_by(ip=assign.ip).one()
                client.credit += credit

Verifier.init()