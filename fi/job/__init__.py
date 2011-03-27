import sys

# directory ROOT_DIRECTORY/jobs for storing server/client jobs/results
JOBS_DIRECTORY = "jobs"
JOB_PORT = 5555
# Maximum amount of jobs to create
MAX_JOBS = 100
# How many instances of each job to wait for in order to verify
MAX_INSTANCES = 3
# Current task
TASK = "diffie_hellman"

import random
random.seed()

HASH_LENGTH = 16

def randomHash():
    """
    None -> str
    """
    
    return "%x" % random.getrandbits(HASH_LENGTH * 4)
    
def partition(l, n):
    """
    l:[_] | n:int -> [[_]]

    """
    division = len(l) / float(n)

    return [
        l[int(round(division * i)): int(round(division * (i + 1)))]
        for i in range(n)
        ]

def createJobs():
    task_directory = os.path.join(fi.ROOT_DIRECTORY, 'job', TASK)
    task_path = os.path.join(task_directory, TASK)
    task_input = os.path.join(task_directory, "jobInput")
    
    task_modules = __import__(TASK)
    
    for i, job_input in enumerate(task_module.input(task_path)):
        write("%d " % i)
        sys.stdout.flush()
        
        # Write job input
        with open(task_input, 'w') as file:
            file.write(job_input)
    
        # Archive job
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