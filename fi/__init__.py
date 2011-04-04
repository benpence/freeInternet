import os
import subprocess

from twisted.internet import reactor

import fi.log

# CONFIG
HOST = "127.0.0.1" # Server IP
SLEEP = 2 # Standard tiem to wait until doing something else

def logmsg(cls, message):
    """Global logging tool"""
    fi.log.log.msg(
        "[%s] %s" % (cls.__name__, message)
    )

def callLater(*args, **kwargs):
    """Call first param from *args later with the rest of the parameters"""
    reactor.callLater(
        SLEEP,
        *args,
        **kwargs
    )

def makeUsage(args, rules):
    """Create usage string for failed args check"""
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
    args:[str] | rules:iter(str) -> str OR False
    
    If each nth element is not in the nth list in rules, return usage else False
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
    
    Execute a shell command and return output from its stdout
    This is only for non-twisted code
    """
    return subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0]

def chain(*args):
    """
    *args:_ -> generator
    
    chains elements and shallow lists together
    """
    for arg in args:
        try:
            lst = iter(arg)
            for item in lst:
                yield item
        except TypeError, e:
            yield arg