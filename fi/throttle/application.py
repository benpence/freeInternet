import os
import math

from twisted.internet import reactor

import fi
import fi.throttle
import fi.throttle.shell
import fi.exception as exception

class ThrottleApplication(object):    
    @classmethod
    def schedule(cls, credits):
        """
        credits:[(str, int)] -> None
        
        """
        print "Scheduling"
        
        max_credit = max(
            credits,
            key=lambda x: x[1]
        )[1]
        
        # This right here is essentially the scheduling, converting the credit to proportional numbers
        logs = [
            (ip,
              math.log1p(credit + 1))
             for (ip, credit) in credits]
            
        total_log = reduce(
            lambda x, y: x + y,
            (n
             for (_, n) in logs)
        )

        allocations = (
            (ip, (log / total_log) * fi.throttle.AVAILABLE_BANDWIDTH)
            for (ip, log) in logs
        )
        
        return allocations
        
    @classmethod
    def throttle(cls, allocations):
        """
        allocations:[(str, int)] -> shell:fi.shell.Shell
        
        """

        print "Making allocations"
        
        shell = fi.throttle.shell.Shell()
        interface = fi.throttle.VPN_INTERFACE
        
        toRun = (
            # Drop current rules
            "/sbin/tc qdisc del dev %s root" % interface,
            "/sbin/iptables -t mangle -F",

            # Create queueing discipline on device root
            "/sbin/tc qdisc add dev %s root handle 1:0 htb" % interface,
            )

        # Run above commands
        for command in toRun:
            shell.add(command)

        # Create node, filter, and /sbin/iptables mark rule for each client
        for i, (ip, allocation) in enumerate(allocations):
            bandwidth = float(allocation) * fi.throttle.BANDWIDTH_HEURISTIC
            # Create classes off of root qdisc
            shell.add("/sbin/tc class add dev %s parent 1: classid 1:%d htb rate %sbps prio %d" % (
                interface, i + 1, bandwidth, i + 1
                )
            )

            # Mark traffic 
            shell.add("/sbin/iptables -t mangle -A POSTROUTING -d %s -j MARK --set-mark %d" % (
                ip, i + 1
                )
            )

            # Filter traffic
            shell.add("/sbin/tc filter add dev %s parent 1:0 protocol ip prio %d handle %d fw flowid 1:%d" % (
                interface, i + 1, i + 1, i + 1
                )
            )
            
        shell.execute()

    @classmethod
    def pathloadReceive(cls):
        """
        None -> None
        
        Calls pathload binary to start measuring bandwidth
        """
        
        shell = fi.throttle.shell.Shell()
        shell.add(
            os.path.join(
                fi.throttle.PATHLOAD_DIRECTORY,
                "pathload/pathload_rcv -s %s | awk '/Available/ {print $5,$7}'" % 
                    fi.throttle.PATHLOAD_CLIENT
            ),
            callback=cls.onPathloadReceive
        )
        
        reactor.callLater(
            fi.SLEEP,
            shell.execute
        )
    
    @classmethod
    def onPathloadReceive(cls, data):
        """
        data:str -> None
        
        Receives bandwidth data in form "float float" and sets max bandwidth
        Calls receive funciton again
        """
        try:
            lines = data.split('\n')
            high = 0
            low = 0
            
            for line in lines:
                if 'Available' in line:
                    words = line.split()
                    low = float(words[4])
                    high = float(words[6])
            
            if high and low:
                available = (high + low) / 8 / 2 * 1000
                print "Setting new available bandwidth to ", available, "kbps"
                # Convert from Mbps to kBps and set to available bandwidth
                
                fi.throttle.AVAILABLE_BANDWIDTH = available
        except ValueError, e:
            print "Unsuccessful parsing for available bandwidth"

        cls.pathloadReceive()

    @classmethod
    def pathloadSend(cls):
        """
        None -> None
        
        Client tests bandwidth with pathload and then adds callback to call itself
        """
        shell = fi.throttle.shell.Shell()
        shell.add(
            os.path.join(
                fi.throttle.PATHLOAD_DIRECTORY,
                "pathload/pathload_snd -i"
            ),
            callback=lambda data: cls.pathloadSend()
        )
        
        reactor.callLater(
            fi.SLEEP,
            shell.execute
        )