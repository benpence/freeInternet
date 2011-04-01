import os
import subprocess

import twisted.internet.defer

# CONFIG
HOST = "127.0.0.1" # Server IP
SLEEP = 2 # Standard tiem to wait until doing something else

try:
    DATABASE_PATH = os.path.join(ROOT_DIRECTORY, "freeInternet.db")
except NameError, e:
    DATABASE_PATH = os.path.join(os.path.abspath('../'), "freeInternet.db")


inlineCallbacks = twisted.internet.defer.inlineCallbacks

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
    
    if len(args) != len(rules) + 1:
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

def chain(*args):
    for arg in args:
        try:
            lst = iter(arg)
            for item in lst:
                yield item
        except TypeError, e:
            yield arg