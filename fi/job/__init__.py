# directory ROOT_DIRECTORY/jobs for storing server/client jobs/results
JOBS_DIRECTORY = "jobs"
JOB_PORT = 5555
# Maximum amount of jobs to create
MAX_JOBS = 100
# How many instances of each job to wait for in order to verify
MAX_INSTANCES = 3
# Current task
TASK = "diffie_hellman"

import random
random.seed()

HASH_LENGTH = 16

def randomHash():
    """
    None -> str
    """
    
    return "%x" % random.getrandbits(HASH_LENGTH * 4)
    
def partition(l, n):
    """
    l:[_] | n:int -> [[_]]

    """
    division = len(l) / float(n)

    return [
        l[int(round(division * i)): int(round(division * (i + 1)))]
        for i in range(n)
        ]