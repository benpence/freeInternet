#!/bin/python

import os
import sqlite
import commands
import time

import sys
sys.path.insert(0, "../../classes")
import server_class

class Throttler:
    _BANDWIDTH = 8000000
    _SLEEP_TIME = 5

    def __init__(self):
        self.databaseConnection = sqlite3.connect("../../database.db")
        self.databaseCursor = self.databaseConnection.cursor()

    def readDatabase(self):
        rows = self.databaseCursor.execute("SELECT client, credit FROM credit")

        return [(row[0], row[1]) for row in rows]

    def schedule(self, credits):
        creditTotal = reduce(lambda x, y : x[1] + y[1], credits)

        return [(client, credit / float(creditTotal)) for client, credit in credits]

    def writeTC(self, allocations):
        interface = "tun0"
        commands.getoutput(
        toRun = [
            # Drop current rules
            "tc qdisc del dev tun0 root",
            "iptables -t mangle -F",

            # Create queueing discipline on device root
            "tc qdisc add dev tun0 root handle 1:0 htb"]
        
        for command in toRun:
            commands.getoutput(command)

        for i, item in enumerate(allocations):
            ip, allocation = item

            # Compensate for encryption
            allocation *= 

            # Create classes off of root qdisc
            commands.getoutput("tc class add dev %s parent 1: classid 1:%d htb rate %sbps prio %d" % (interface, i + 1, allocation * 10 / 9., i + 1))
        
            # Mark traffic 
            commands.getoutput("iptables -t mangle -A POSTROUTING -d %s  -j MARK --set-mark %d" % (ip, i + 1))

            # Filter
            commands.getoutput("tc filter add dev %s parent 1:0 protocol ip prio %d handle %d fw flowid 1:%d" % (interface, i + 1, i + 1, i + 1))

def Main():
    throttler = Throttler()
    
    try:
        while True:
            credits = throttler.readDatabase()
            allocations = throttler.schedule(credits)
            throttler.writeTC(allocations)
    except KeyboardInterrupt:
        print "Exiting..."

if __name__ = "__main__":
    Main()
