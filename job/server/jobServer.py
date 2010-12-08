#!/usr/bin/python

import os
import sqlite3


import sys
sys.path.insert(0, "../../classes")
import server_class

class ServerJob(server_class.Server):

    def __init__(self):
        super(ServerJob, self).__init__(jobDirectory=os.path.join(os.getcwd(), "jobs"), getJobIDFunction=self.newJob, updateDatabase=self.oldJob)

        self.databaseConnection = sqlite3.connect('database.db')
        self.databaseCursor = self.databaseConnection.cursor()

    def newJob(self, client):
        row = self.databaseCursor.execute("SELECT id, instance FROM status WHERE client ISNULL LIMIT 1").fetchone()

        # Give first job if no more jobs to complete
        if not row:
           row = self.databaseCursor.execute("SELECT id, instance FROM status LIMIT 1").fetchone()

        self.databaseCursor.execute("UPDATE status SET client = ?, accepted_datetime = DATETIME('NOW') WHERE id = ? AND instance = ?", (str(client), row[0], row[1]))

        self.databaseConnection.commit()

        return int("%d%d" % row)

    def oldJob(self, client, jobID):
        self.databaseCursor.execute("UPDATE status SET returned_datetime = DATETIME('NOW') WHERE id = ? AND instance = ?", (jobID / 10, jobID % 10))

        credit = self.databaseCursor.execute("SELECT credit FROM job WHERE id = ?", (str(jobID / 10))).fetchone()[0]
        self.databaseCursor.execute("UPDATE credit SET credit = credit + ? WHERE client = ?", (str(credit), str(client)))

        self.databaseConnection.commit()
    def __str__(self):
        return "job_server"

    #def log(self, *args, **kargs):
        #if 'output' not in kargs:
            #kargs['output'] = self.output
#
        #logging.Logger.log(*args, **kargs)

def Main():
    server = ServerJob()
    server.listen()

if __name__ == "__main__":
    Main()
