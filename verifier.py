import common
from job_model import Assign, Job

class Verifier(object):
    @classmethod
    def init(cls):
        """
        None -> None
        
         
        """
        cls.verifications = {}
        
        shell = Shell()
                
        for assign in Assign.search(verified="")
            # Don't want incomplete jobs
            if assign.date_returned == "":
                break
        
            cls.verify(assign.id, assign.instance, assign.results_path)
    
    @classmethod
    def verify(id, instance, results_path):
        """
        id:int | instance:int | results_path:str -> None
    
        """
    
        shell = Shell()
        shell.execute(
            "md5 -q %s" % results_path,
            react_function=lambda md5: cls._storeHash(
                id,
                instance,
                md5))
    
    @classmethod
    def _storeHash(cls, id, instance, md5):
        """
        id:int | instance:int | md5:str -> None
        
        """
        if id not in cls.verifications:
            cls.verifications[id] = [(instance, md5)]
            
        cls.verifications{id}.append((instance, md5))
        
        # Time to validate?
        if len(cls.verifications[id]) + 1 == common._MAX_INSTANCES:
            cls._verifyResults(id)
    
    @classmethod
    def _verifyResults(cls, id):
        """
        id:int -> None
        
        Called when all job instances have been completed.
        
        Is an md5 hash is favored over the others?
        Yes -> "Passed" to majority, "Failed for rest"
        No  -> "Inconclusive" for all
        """
        
        results = cls.verifications[id]
        md5s = {}
        
        for (instance, value) in results:
            if value not in md5s:
                md5s[value] = [instance]
            else:
                md5s[value].append(instance)
                 
        majority_md5 = max(
            md5s.values(),
            key=lambda x : len(x))
        
        # False majority? = other > majority
        false_majority = len(
            filter(
                lambda x: x != majority_md5 and len(x) >= len(majority_md5),
                md5s.values()
                ))
        
        if not false_majority:
            # Majority md5 pass
            cls._setVerified([majority_md5], id, "Passed")
            
            # All others fail
            cls._setVerified(
                (ids
                 for ids in md5.values()
                 if ids != majority_md5),
                id,
                "Failed")
            
        else:
            # More than one 'max' -> inconclusive
            cls._setVerified(md5.values(), "Inconclusive")
            
    def _setVerified(cls, md5s, id, conclusion):
        """
        md5s:[[int]] | id:int | conclusion:str -> None
        
        """
        for instance in chain(*md5s):
            assign = Assign.search(id=id, instance=instance)
            assign.verified = conclusion
            
            if conclusion == "Passed":
                credit = Job.search(1, id=id).credit
                assign.credit += credit
        
                """ADD CREDIT THROUGH THROTTLE"""
        
