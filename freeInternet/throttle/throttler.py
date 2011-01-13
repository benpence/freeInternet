import os
import sqlite3
import commands
import time

#import sys
#sys.path.insert(0, "../../classes")

class Throttler:
    _BANDWIDTH = 4000000
    _SLEEP_TIME = 5

    def __init__(self):
        self.databaseConnection = sqlite3.connect("../database.db")
        self.databaseCursor = self.databaseConnection.cursor()

    def readDatabase(self):
        translations = dict(self.databaseCursor.execute("SELECT * FROM translation").fetchall())
        credits =      dict(self.databaseCursor.execute("SELECT * FROM credit"     ).fetchall())

        return [(key, credits[translations[key]]) for key in translations if credits[translations[key]] > 0]

    def schedule(self, credits):
        creditTotal = reduce(lambda x, y : x[1] + y[1], credits)

        return [(client, int(credit / float(creditTotal) * Throttler._BANDWIDTH)) for client, credit in credits] 

    def writeTC(self, allocations):
        interface = "tun0"
        toRun = [
            # Drop current rules
            "tc qdisc del dev tun0 root",
            "iptables -t mangle -F",

            # Create queueing discipline on device root
            "tc qdisc add dev tun0 root handle 1:0 htb"]
        
        # Run above commands
        for command in toRun:
            commands.getoutput(command)

        # Create node, filter, and iptables mark rule for each client
        for i, item in enumerate(allocations):
            ip, allocation = item

            # Create classes off of root qdisc
            commands.getoutput("tc class add dev %s parent 1: classid 1:%d htb rate %.0dbps prio %d" % (interface, i + 1, allocation * 10 / 9., i + 1))
        
            # Mark traffic 
            commands.getoutput("iptables -t mangle -A POSTROUTING -d %s  -j MARK --set-mark %d" % (ip, i + 1))

            # Filter
            commands.getoutput("tc filter add dev %s parent 1:0 protocol ip prio %d handle %d fw flowid 1:%d" % (interface, i + 1, i + 1, i + 1))

def Main():
    throttler = Throttler()
    
    try:
        while True:
            print "Reading database..."
            credits = throttler.readDatabase()
            print credits
            print "Creating Schedule..."
            allocations = throttler.schedule(credits)
            print allocations
            print "Running commands...\n"
            throttler.writeTC(allocations)
            time.sleep(Throttler._SLEEP_TIME)
    except KeyboardInterrupt:
        print "Exiting..."

if __name__ == "__main__":
    Main()
