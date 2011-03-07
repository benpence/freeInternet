import commands
import sys
import os

write = sys.stdout.write

try:
    import sqlite3 as sqlite
except ImportError, e:
    import sqlite
    
import freeInternet.common as common
import freeInternet.job.model
import freeInternet.throttle.model

write("Deleting old database...")
commands.getoutput("rm -f %s" % common._DATABASE_PATH)
print "done."

write("Creating tables...")
freeInternet.throttle.model.__setup__()
freeInternet.job.model.__setup__()
print "done."

write("Replacing file directories... ")
commands.getoutput("rm -rf %s" % common._SERVER_DIRECTORY)
commands.getoutput("mkdir %s" %  common._SERVER_DIRECTORY)
commands.getoutput("rm -rf %s" % common._CLIENT_DIRECTORY)
commands.getoutput("mkdir %s" %  common._CLIENT_DIRECTORY)
print "done."

#write("Compiling 'job.c'... ")
commands.getoutput("rm -f job")
commands.getoutput("gcc -o job job.c > /dev/null")
#print "done."

print "Creating jobs:"
for i in range(common._MAX_JOBS):
    write("%d " % i)
    sys.stdout.flush()
    
    commands.getoutput("echo %d > jobInput" % i)
    commands.getoutput("tar czvf %d jobInput job.c > /dev/null" % i)
    commands.getoutput("mv %d %s" % (
        i,
        common._SERVER_DIRECTORY))
    
commands.getoutput("rm -f jobInput job")
print
#commands.getoutput("rm -f server_files/* && cp backup/* server_files")

write("Creating logs directory...")
commands.getoutput("mkdir logs")
print "done."
