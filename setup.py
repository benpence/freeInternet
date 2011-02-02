import commands
import sys
import os

write = sys.stdout.write

try:
    import sqlite3 as sqlite
except ImportError, e:
    import sqlite
    
import common
import job_model

write("Deleting old database...")
commands.getoutput("rm -f %s" % common._DATABASE_PATH)
print "done."

write("Creating tables...")
job_model.__setup__()
print "done."

write("Replacing file directories... ")
commands.getoutput("rm -rf %s" % common._SERVER_DIRECTORY)
commands.getoutput("mkdir %s" %  common._SERVER_DIRECTORY)
commands.getoutput("rm -rf %s" % common._CLIENT_DIRECTORY)
commands.getoutput("mkdir %s" %  common._CLIENT_DIRECTORY)
print "done."

write("Compiling 'job.c'... ")
commands.getoutput("rm job")
commands.getoutput("gcc -o job job.c > /dev/null")
print "done."

print "Creating jobs:"
for i in range(common._MAX_JOBS):
    write("%d " % i)
    sys.stdout.flush()
    
    commands.getoutput("echo %d > jobInput" % i)
    commands.getoutput("tar czvf %d jobInput job > /dev/null" % i)
    commands.getoutput("mv %d %s" % (
        i,
        common._SERVER_DIRECTORY))
    
commands.getoutput("rm -f jobInput job")
print

"""
    "INSERT INTO credit VALUES('128.164.160.198', 0);"
    "INSERT INTO credit VALUES('128.164.160.199', 0);"

    "INSERT INTO translation VALUES('10.8.0.10', '128.164.160.198');"
    "INSERT INTO translation VALUES('10.8.0.6',  '128.164.160.199');"
    )
"""
