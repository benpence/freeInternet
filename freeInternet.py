#!/usr/bin/env python

import sys
import commands
import os

def execute(command):
    return commands.getoutput(command)

def start(module, app):
    execute(
        "twistd -y freeInternet/%s/%s.tac --pidfile=%s_%s.pid --logfile=logs/%s_%s" % (
            module, app,
            module, app,
            module, app
        )
    )
    
    pid = open(module + "_" + app + ".pid", 'r').read().strip()
    
    print "%s %s started with pid %s" % (
        module,
        app,
        pid
    )

def start_test(module, app):
    print execute(
        "twistd -ny freeInternet/%s/%s.tac --pidfile=%s_%s.pid" % (
            module, app,
            module, app,
        )
    )

def stop(module, app):
    pid_file = module + "_" + app + ".pid"

    if not os.path.exists(pid_file):
        return
        
    pid = open(pid_file, 'r').read().strip()
    execute("kill " + pid)
    
    print "%s %s killed with pid %s" % (
        module,
        app,
        pid
    )

def restart(module, app):
    stop(module, app)
    start(module, app)
    
def status(module, app):
    pid_file = module + "_" + app + ".pid"
    
    if not os.path.exists(pid_file):
        print "%s %s not running" % (
            module,
            app
        )
    else:
        pid = open(pid_file).read().strip()
        print "%s %s running with pid %s" % (
            module,
            app,
            pid
        )

modules_to_apps = {
    "job": ("client", "server"),
    "throttle": ("server"),
    "web": ("server"),
}

actions = {
    "start": start,
    "start_test": start_test,
    "stop": stop,
    "restart": restart,
    "status": status,
}

def usage():
    print "Usage: %s {%s} {%s}" % (
        sys.argv[0],
        '|'.join(modules_to_apps.keys()),
        '|'.join(actions.keys())
    )
    exit(0)

def Main():
    # Check length
    if len(sys.argv) is not 4:
        usage()
        
    # Check module
    elif sys.argv[1] not in modules_to_apps:
        usage()
    
    module = sys.argv[1]
    
    # Check app
    if sys.argv[2] not in modules_to_apps[module]:
        usage()
    
    app = sys.argv[2]
    
    # Check action
    if sys.argv[3] not in actions:
        usage()
    
    # Add module to path
    sys.path.append('.')
    
    # Perform action
    actions[sys.argv[3]](module, app)
    
if __name__ == "__main__":
    Main()