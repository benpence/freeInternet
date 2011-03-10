
import sys
import commands
import os

execute = commands.getoutput

def start(slash, dot):
    
    
    execute(
        "twistd -y %s.tac --pidfile=%s.pid --logfile=logs/%s" % (
            os.path.join(_ROOT_DIRECTORY, 'freeInternet', slash),
            dot,
            dot
        )
    )
    
    pid = open(dot + ".pid", 'r').read().strip()
    
    print "%s started with pid %s" % (
        dot,
        pid
    )

def start_test(slash, dot):
    print execute(
        "twistd -ny %s.tac --pidfile=%s.pid" % (
            os.path.join(_ROOT_DIRECTORY, 'freeInternet', slash),
            dot
        )
    )

def stop(slash, dot):
    pid_file = dot + ".pid"

    if not os.path.exists(pid_file):
        return
        
    pid = open(pid_file, 'r').read().strip()
    execute("kill " + pid)
    
    print "%s killed with pid %s" % (
        dot,
        pid
    )

def restart(slash, dot):
    stop(slash, dot)
    start(slash, dot)
    
def status(slash, dot):
    pid_file = dot + ".pid"
    
    if not os.path.exists(pid_file):
        print "%s not running" % (
            dot
        )
    else:
        pid = open(pid_file).read().strip()
        print "%s running with pid %s" % (
            dot,
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

def main():
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
    name_slash = '/'.join((module, app))
    name_dot = '.'.join((module, app))
    actions[sys.argv[3]](name_slash, name_dot)
    
if __name__ == "__main__":
    main()