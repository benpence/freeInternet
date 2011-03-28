import commands
import sys
import os
import itertools

import fi
fi.ROOT_DIRECTORY = os.getcwd()
import fi.job
import fi.model
import fi.job.model
import fi.throttle.model

def _prepend(filename, prefix, action):
    # Read
    with open(filename, 'r') as f:
        text = f.read()

    added = prefix in text

    if action == 'install':
        if added:
            return

        text = prefix + text
   
    else:
        if not added:
            return
    
        text = text.replace(prefix, '')
    
    # Write if necessary
    with open(filename, 'w') as f:
        f.write(text)

def doPaths(action):
    # Add path so process can find fi package
    print "Setting application paths..."
    SCRIPTS = (
        'fi/job/client.py',
        'fi/job/server.py',
        'fi/throttle/client.py',
        'fi/throttle/server.py',
        'fi/web/server.py',
        'freeInternet.py',
    )

    prefix = "import sys\nsys.path.append('%s')\n" % fi.ROOT_DIRECTORY
    
    for filename in SCRIPTS:
        _prepend(
            filename,
            prefix,
            action
        )
    
    print "Setting directory for database..."
    _prepend(
        'fi/__init__.py',
        'ROOT_DIRECTORY = "%s"\n' % fi.ROOT_DIRECTORY,
        action
    )

def doDatabase(action):
    if os.exists(fi.DATABASE_PATH):
        print "Deleting old database..."
        fi.execute("rm -f " + fi.DATABASE_PATH)
    
    # Install    
    if action == 'install':
        print "Creating tables..."
    
        fi.model.createDatabaseTables()
        fi.job.model.setup()
        fi.throttle.model.setup()

def doLogs(action):
    if os.exists('logs'):
        print "Deleting logs directory..."
        fi.execute('rm -rf logs')
        
    if action == 'install':
        print "Creating logs directory..."
        fi.execute("mkdir logs")

def main():
    modules = {
        'server': (
            doDatabase,
        ),
        'client': (),
    }
    actions = (
        'install',
        'uninstall',
    )
    
    usage = fi.invalidArguments(
        sys.argv,
        (modules, actions)
    )
    
    if usage:
        print usage()
        exit(1)
    
    for func in fi.chain(doPaths, modules[argv[1]], doLogs):
        func(argv[2])

if __name__ == '__main__':
    main()