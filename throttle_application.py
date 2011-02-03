import math

import common


class ThrottleApplication(object):    
    @classmethod
    def schedule(cls, credits):
        """
        credits:[(str, int)] -> None
        
        """
        
        max_credit = max(
            credits,
            key=lambda x: x[1])[1]
        
        # This right here is essentially the scheduling, converting the credit to proportional numbers
        numbers = [
            ((ip,
              math.log1p(credit + 1) * math.sqrt(max_credit))
             for (ip, credit) in credits)]
            
        total_number = sum(
            numbers,
            key=lambda x: x[1]
        )
        
        allocations = (
            ((ip,
              number / total_number)
             for (ip, number) in numbers)
        )
        
        return allocations
        
    @classmethod
    def throttle(cls, allocations):
        """
        allocations:[(str, int)] -> shell:common.Shell
        
        """
        
        shell = common.Shell()
        interface = common._VPN_INTERFACE
        
        toRun = (
            # Drop current rules
            "tc qdisc del dev %s root" % interface,
            "iptables -t mangle -F",

            # Create queueing discipline on device root
            "tc qdisc add dev %s root handle 1:0 htb" % interface,
            )

        # Run above commands
        for command in toRun:
            shell.execute(command)

        # Create node, filter, and iptables mark rule for each client
        for i, (ip, allocation) in enumerate(allocations):
            # Create classes off of root qdisc
            shell.execute("tc class add dev %s parent 1: classid 1:%d htb rate %.0dbps prio %d" % (
                interface,
                i + 1,
                allocation * common._BANDWIDTH_HEURISTIC,
                i + 1))

            # Mark traffic 
            shell.execute("iptables -t mangle -A POSTROUTING -d %s -j MARK --set-mark %d" % (
                ip,
                i + 1))

            # Filter
            shell.execute("tc filter add dev %s parent 1:0 protocol ip prio %d handle %d fw flowid 1:%d" % (
                interface,
                i + 1,
                i + 1,
                i + 1))
            
        return shell