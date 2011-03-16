import commands
import sys
import os

import fi
import fi.job
import fi.job.model
import fi.throttle.model

write = sys.stdout.write
execute = commands.getoutput

def prepend(filename, prefix):
    f = open(filename, 'r')
    text = prefix + f.read()
    f.close()
    
    f = open(filename, 'w')
    f.write(text)
    f.close()

def setPaths():
    prefix = "ROOT_DIRECTORY = '%s'\n" % os.getcwd()
    
    for f in ('freeInternet.py', 'freeInternet/__init__.py'):
        prepend(
            f,
            prefix,
        )

def removeDatabase():
    write("Deleting old database...")
    execute("rm -f %s" % fi.DATABASE_PATH)
    print "done."

    write("Creating tables...")
    fi.throttle.model.__setup__(
        fi.job.TASK_DIRECTORY
    )
    fi.job.model.__setup__()
    print "done."

def createJobDirectory():
    write("Replacing file directories... ")
    
    execute("rm -rf %s" % fi.job.JOBS_DIRECTORY)
    execute("mkdir %s" %  fi.job.JOBS_DIRECTORY)
    print "done."

def createJobs():
    task_directory = os.path.join(fi.ROOT_DIRECTORY, *fi.job.TASK_DIRECTORY)
    task_path = os.path.join(task_directory, "job")
    task_input = os.path.join(task_directory, "jobInput")

    print "Creating jobs:"
    task_module = __import__(
        '.'.join(fi.job.TASK_DIRECTORY + [fi.job.TASK])
    )
    
    for i, job_input in enumerate(task_module.input(fi.job.MAX_JOBS, task_path)):
        write("%d " % i)
        sys.stdout.flush()
        
        with open(os.path.join(task_directory, fi.job.TASK), 'w') as file:
            file.write(job_input)
    
        # Archive current job
        execute("tar czvf %d %s %s > /dev/null" % (
            i,
            task_input,
            "%.c" % task_path
            )
        )
        
        # Move it to jobs directory
        execute("mv %d %s" % (
            i,
            fi.job.JOBS_DIRECTORY))
    
    execute("rm -f jobInput job")
    print

def createLogsDirectory():
    write("Creating logs directory...")
    execute("mkdir logs")
    print "done."

def main():
    modules = {
        'server': (
            removeDatabase,
            createJobDirectory,
            createJobs,
            createLogsDirectory
        ),
        'client': (
            createJobsDirectory,
            createLogsDirectory
        )
    }
    actions = ('install', 'uninstall')
    
    usage = fi.invalidArguments(
        sys.args,
        (modules, actions)
    )
    
    if usage:
        print usage()
        exit(1)
    
    for func in modules[sys.args[1]]:
        func()    

if __name__ == '__main__':
    main()