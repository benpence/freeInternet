import os
import sys


# If dirs not in path, add to path


def server(action):
    pass

def client(action):
    pass

def throttle(action):
    pass

modules = {"server" : server,
           "client" : client,
           "throttle" : throttle}
actions = ["start", "stop", "status"]

def Main(module, action):
    try:
        modules[module](action)
    except Exception, e:
        print e

def usage():
    modules_string = '{' + '|'.join(modules.keys()) + '}'
    actions_string = '{' + '|'.join(actions) + '}'

    print "Usage: FI.py %s %s" % (modules_string, actions_string)
    exit()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()

    if sys.argv[1] not in modules or sys.argv[2] not in actions:
        usage()

    Main(*sys.argv[1:])
