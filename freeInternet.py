import os

import fi

def start(module):
    fi.execute(
        "twistd -y %s.tac --pidfile=%s.pid --logfile=logs/%s" % (
            os.path.join(fi.ROOT_DIRECTORY, 'fi', slash),
            module, 
            module,
        )
    )
    
    pid = open(module + ".pid", 'r').read().strip()
    print "%s started with pid %s" % (module, pid)

def start_test(module):
    print fi.execute(
        "python %s.tac" % (
            os.path.join(fi.ROOT_DIRECTORY, 'fi', slash),
            dot
        )
    )

def stop(module):
    pid_file = dot + ".pid"

    if not os.path.exists(pid_file):
        return
        
    pid = open(pid_file, 'r').read().strip()
    fi.execute("kill " + pid)
    
    print "%s killed with pid %s" % (
        dot,
        pid
    )

def restart(module):
    stop(module)
    start(module)
    
def status(module):
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

modules = (
    "server",
    "client",
)

actions = {
    "start": start,
    "start_test": start_test,
    "stop": stop,
    "restart": restart,
    "status": status,
}

def main():    
    usage = fi.invalidArgs(
        sys.argv,
        (modules, actions),
    )
    
    if usage:
        print usage
        exit(1)
    
    module, action = sys.argv[:2]
    
    # Perform action
    actions[action](module)
    
if __name__ == "__main__":
    main()