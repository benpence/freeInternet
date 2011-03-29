import sys
import os

JOB_PORT = 5555

MAX_JOBS = 100 # Maximum amount of jobs to create
MAX_INSTANCES = 3 # Instances of each job to wait for in order to verify

TASK = "DiffieHellman" # Current task

HASH_LENGTH = 16

import random
random.seed()

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