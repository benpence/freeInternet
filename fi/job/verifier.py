import itertools
import hashlib

import fi.job
import fi.model as model
from fi.job.model import Assignment, Instance, Job

class Verifier(object):
    digests = {} # Waiting to be verified
    done = {} # For repeats
    
    messages = ('Incorrect', 'Correct')
    
    @classmethod
    def init(cls):
        """
        None -> None
        """
        for instance in Instance.query.all():
            if instance.digest:
                cls.done[(instance.job, instance)] = instance.digest
        
        for assignment in Assignment.query.filter_by(verified=None).all():
            # Needs to be verified?
            if assignment.date_returned:
                cls.verify(assignment)
                
    
    @classmethod
    def verify(cls, assignment):
        """
        assign:Assignment -> None
        """
        key = (assignment.job, assignment.instance)
        
        # A repeat -> compare verified hash to new hash
        if key in cls.done:
            assignment.verified = cls.messages[
                hash(assignment.output) == assignment.instance.digest
            ]
        
        # Create new list or append?
        cls.digests.setdefault(key, []).append(assignment)

        # Time to verify all?
        if len(cls.digests[key]) == fi.job.MAX_ASSIGNMENTS:
            cls._verifyResults(key)

    @classmethod
    def _verifyResults(cls, key):
        """
        id:int -> None
        
        Called when all job instances have been completed.
        
        Is a hash is favored over the others?
        Yes -> "Correct" to majority, "Incorrect for rest"
        No  -> "Inconclusive" for all
        """
        fi.logmsg(cls, "Verifying %d-%d" % tuple(map(lambda x: x.id, key)))
        
        assignments = cls.digests[key]
        votes = {}
        
        for assignment in assignments:
            o = hash(assignment.output)
            votes.setdefault(o, []).append(assignment)
        
        majority_digest = max(votes, key=lambda o: len(votes[o]))
        
        # False majority? other >= majority
        false_majority = len(
            filter(
                lambda x: x != majority_digest and len(votes[x]) >= len(votes[majority_digest]),
                votes
            )
        )

        # Set verified status
        if false_majority:
            for ass in assignments:
                ass.reset()
        else:
            # Cache correct result hash
            cls.done[key] = majority_digest
            key[1].digest = majority_digest
            
            for ass in assignments:
                correct = hash(ass.output) == majority_digest
            
                ass.verified = cls.messages[correct]
                
                if correct:
                    ass.client.credit += ass.job.credit

        del cls.digests[key]

        model.commit()

Verifier.init()