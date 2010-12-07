#!/bin/bash -e

# Global variables
DATABASE_NAME="database.db"

JOB_START=0
JOB_END=2
JOB_INSTANCE_START=0
JOB_INSTANCE_END=3

CLIENT_START=197
CLIENT_END=199

# Fill database with scheme:
#
#    Jobs
#        ID
#        Credit
#
#    Job Status
#        ID
#        Instance
#
#        Location Job
#
#        Client
#        Accepted Timestamp
#
#        Returned Timestamp
#        Location Output
#
#        Verified\\\
#
#    Credits
#        Client
#        Credit

function print(){
    echo -ne "$1"
}

print "Deleting old database... "
rm $DATABASE_NAME
print "done.\n"

print "Creating tables... "
sqlite3 $DATABASE_NAME << SQL_ENTRY_TAG_2

CREATE TABLE job(
    id              INTEGER PRIMARY KEY NOT NULL,
    credit          INTEGER,
    description     VARCHAR
);

CREATE TABLE status(
    id              INTEGER NOT NULL,
    instance        INTEGER NOT NULL,

    client          VARCHAR,

    accepted_time   DATETIME,
    returned_time   DATETIME,

    PRIMARY KEY(id, instance)
);


CREATE TABLE credit(
    client          VARCHAR PRIMARY KEY,
    credit          INTEGER
);

SQL_ENTRY_TAG_2

print "done.\n"


### Create job binary ###
print "Replacing 'jobs' folder... "
rm -rf jobs
mkdir jobs
print "done.\n"


print "Compiling job... "
gcc -o job job.c > /dev/null
print "done.\n"


### Create jobs ###
print "Creating jobs.\n"
for i in {$JOB_START..$JOB_END}; do
    # Insert for job
    command="\tINSERT INTO jobs VALUES($i, 5, 'Copy 1000 times input');\n"
    print "$command"
    sqlite3 $DATABASE_NAME "$command"


    for j in {$JOB_INSTANCE_START..$JOB_INSTANCE_END}; do
        # Insert for job instance
        command="\t\tINSERT INTO status VALUES($i, $j, NULL, NULL, NULL);\n"
        print "$command"
        sqlite3 $DATABASE_NAME "$command"

        # Create file
        print "\t\tPackaging job... "
        dir=jobs/$i$j
        mkdir $dir
        cp ./job $dir
        echo "$i" > $dir/jobInput
        tar czvf $dir.send.tgz $dir > /dev/null
        rm -rf $dir
        print "done.\n"
    done
done

print "\n"

### Insert clients ###
#print "Creating clients."
#for i in {$CLIENT_START..$CLIENT_END}; do
    #command="INSERT INTO credit VALUES("
    #sqlite3 $DATABASE_NAME 

print "\n"

### Clean-up ###
print "Removing job binary... "
rm job
print "done.\n"
