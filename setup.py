import os
import sys
write = sys.stdout.write

try:
    import sqlite3 as sqlite
except ImportError, e:
    import sqlite
    print "'import sqlite3' failed. Using sqlite"
    
import common
import job_model

write("Deleting old database...")
os.system("rm -f %s" % common._DATABASE_PATH)
print "done."

write("Creating tables...")
job_model.__init__()
print "done."

write("Replacing file directories... ")
os.system("rm -rf %s" %     common._SERVER_DIRECTORY)
os.system("mkdir jobs %s" % common._SERVER_DIRECTORY)
os.system("rm -rf %s" % common._CLIENT_DIRECTORY)
os.system("mkdir %s" %  common._CLIENT_DIRECTORY)
print "done."

write("Compiling 'job.c'... ")
os.system("gcc -o job job.c > /dev/null")
print "done."

print "Creating jobs:"
for i in range(common._MAX_JOBS):
    write("\tPackaging job %d... " % i)
    
    os.system("echo %d > jobInput" % i)
    os.system("tar czvf %d jobInput job" % i)
    os.system("mv %d %s" % (
        i,
        common._SERVER_DIRECTORY))
    
    print "done."
os.system("rm -f jobInput job")

"""
    "INSERT INTO credit VALUES('128.164.160.198', 0);"
    "INSERT INTO credit VALUES('128.164.160.199', 0);"

    "INSERT INTO translation VALUES('10.8.0.10', '128.164.160.198');"
    "INSERT INTO translation VALUES('10.8.0.6',  '128.164.160.199');"
    )
"""
