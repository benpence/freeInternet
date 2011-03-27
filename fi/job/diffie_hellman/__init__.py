import commands
import os
import itertools
import random

import fi
import fi.job

import roots

DESCRIPTION = "A brute force attack against a Diffie-Hellman-Merkle Key Exchange"
CREDIT = 5

def input(binary_path, *args):
    # For each prime,primitive-root pair
    for prime, root in itertools.islice(roots.generateRoots(), fi.job.MAX_JOBS):
        # Calculate public keys
        Ay, By = fi.execute("%s %d %d %d %d" % (
            binary_path,
            prime, root,
            random.randint(1, prime - 1), #Ax
            random.randint(1, prime - 1)  #Bx
        )).strip().split()
        
        # Split up input
        for partition in fi.job.partition(range(1, prime + 1), fi.job.MAX_INSTANCES):
            yield ' '.join((str(prime), str(root), Ay, By, str(partition[0]), str(partition[-1])))