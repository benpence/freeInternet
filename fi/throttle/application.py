import math

from twisted.python import log
from twisted.internet import reactor

import fi.throttle
import fi.shell
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
            key=lambda x: x[1])[1]
        
        # This right here is essentially the scheduling, converting the credit to proportional numbers
        numbers = [
            (ip,
              math.log1p(credit + 1) * math.sqrt(max_credit))
             for (ip, credit) in credits]
            
        total_number = reduce(
            lambda x, y: x + y,
            (n
             for (_, n) in numbers)
        )

        allocations = ((ip, number / total_number * fi.throttle.MAX_BANDWIDTH)
             for (ip, number) in numbers)
        
        return allocations
        
    @classmethod
    def throttle(cls, allocations):
        """
        allocations:[(str, int)] -> shell:fi.shell.Shell
        
        """

        print "Making allocations"
        
        shell = fi.shell.Shell()
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
            # Create classes off of root qdisc
            shell.add("/sbin/tc class add dev %s parent 1: classid 1:%d htb rate %sbps prio %d" % (
                interface,
                i + 1,
                str(allocation * fi.throttle.BANDWIDTH_HEURISTIC),
                i + 1
                )
            )

            # Mark traffic 
            shell.add("/sbin/iptables -t mangle -A POSTROUTING -d %s -j MARK --set-mark %d" % (
                ip,
                i + 1
                )
            )

            # Filter traffic
            shell.add("/sbin/tc filter add dev %s parent 1:0 protocol ip prio %d handle %d fw flowid 1:%d" % (
                interface,
                i + 1,
                i + 1,
                i + 1
                )
            )
            
        shell.execute()

    @classmethod
    def pathloadReceive(cls):
        """
        None -> None
        
        Calls pathload binary to start measuring bandwidth
        """
        
        shell = fi.shell.Shell()
        shell.add(
            "pathload/pathload_rcv -s %s | awk '/Available/ {print $5,$7}'" % fi.throttle.PATHLOAD_CLIENT,
            function=cls.onPathloadReceive
        )
        
        reactor.callLater(
            fi.throttle.THROTTLE_SLEEP,
            shell.execute
        )
    
    @classmethod
    def onPathloadReceive(cls, data):
        """
        data:str -> None
        
        Receives bandwidth data in form "float float" and sets max bandwidth
        Calls receive funciton again
        """
        # Acceptable error message:  "Make sure that pathload_snd runs at sender:: Connection refused"
        if data.startswith("Make"):
            raise exception.ConnectionError("pathload_rcv: Cannot connect to %s" % fi.throttle.PATHLOAD_CLIENT)

        else:
            low, high = data.strip().split()
            fi.throttle.MAX_BANDWIDTH = (float(high) + float(low)) / 2

        cls.pathloadReceive()

    @classmethod
    def pathloadSend(cls):
        """
        None -> None
        
        Client tests bandwidth with pathload and then adds callback to call itself
        """
        shell = fi.shell.Shell()
        shell.add(
            "pathload/pathload_snd -i",
            function=lambda data: cls.pathloadSend()
        )
        
        reactor.callLater(
            fi.throttle.THROTTLE_SLEEP,
            shell.execute
        )