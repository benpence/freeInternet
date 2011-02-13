import math
from twisted.python import log

import common


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

        allocations = ((ip, number / total_number * common._MAX_BANDWIDTH)
             for (ip, number) in numbers)
        
        return allocations
        
    @classmethod
    def throttle(cls, allocations):
        """
        allocations:[(str, int)] -> shell:common.Shell
        
        """

        print "Making allocations"
        
        shell = common.Shell()
        interface = common._VPN_INTERFACE
        
        toRun = (
            # Drop current rules
            "/sbin/tc qdisc del dev %s root" % interface,
            "/sbin/iptables -t mangle -F",

            # Create queueing discipline on device root
            "/sbin/tc qdisc add dev %s root handle 1:0 htb" % interface,
            )

        # Run above commands
        for command in toRun:
            shell.execute(command)

        # Create node, filter, and /sbin/iptables mark rule for each client
        for i, (ip, allocation) in enumerate(allocations):
            # Create classes off of root qdisc
            shell.execute("/sbin/tc class add dev %s parent 1: classid 1:%d htb rate %sbps prio %d" % (
                interface,
                i + 1,
                str(allocation * common._BANDWIDTH_HEURISTIC),
                i + 1))

            # Mark traffic 
            shell.execute("/sbin/iptables -t mangle -A POSTROUTING -d %s -j MARK --set-mark %d" % (
                ip,
                i + 1))

            # Filter
            shell.execute("/sbin/tc filter add dev %s parent 1:0 protocol ip prio %d handle %d fw flowid 1:%d" % (
                interface,
                i + 1,
                i + 1,
                i + 1))
            
        return shell
