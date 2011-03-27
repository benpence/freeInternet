ROOT_DIRECTORY = "/Users/ben/Source/freeInternet/fi"

import os
import subprocess

# Model
CHANGES_BEFORE_WRITE = 3 # How many rows changed until write to database
DATABASE_PATH = os.path.join(ROOT_DIRECTORY, "freeInternet.db")

# Server IP
HOST = "127.0.0.1"
# How many bytes to transfer per send/rcv
CHUNK_SIZE = 512

def isNumber(number):
    try:
        float(number)
        return True
    except TypeError:
        return False
    except ValueError:
        return False

def makeUsage(args, rules):
    return "Usage: " + args[0] + ' ' + ' '.join(
        ('{%s}' % '|'.join(
            (
                x 
                for x in rule
            ))
        for rule in rules
        )
    )

def invalidArgs(args, rules):
    """
    args:[str] | rules:([]/{}) -> bool
    """
    
    usage = lambda: makeUsage(args, rules)
    
    if len(args) is not len(rules) + 1:
        return usage
    
    for i, rule in enumerate(rules):
        if args[i + 1] not in rule:
            return usage
    
    return False
    
def execute(command):
    """
    command:str -> str
    
    Execute an 'sh' command and return output from its stdout
    """
    return subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]