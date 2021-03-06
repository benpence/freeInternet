import sys
import random
import itertools

from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import log

import fi.job

class RemoteJob(pb.Referenceable):
    DESCRIPTION = ""
    CREDIT = 0
    
    @classmethod
    def remote_getOutput(cls):
        pass
        
    @classmethod
    def input(cls):
        pass

class DiffieHellman(RemoteJob):
    # About Task
    DESCRIPTION = "A brute force attack against a Diffie-Hellman-Merkle Key Exchange"
    CREDIT = 5
    
    # Constants
    MIN_PRIME = 2 # First prime is 2. DON'T CHANGE THIS
    MIN_MOD = 2000 # Start giving moduli at this number and above

    # Globals
    primes = []
    
    def remote_getOutput(self, p, g, Ay, By, start, stop):
        # Try all stop->stop private keys
        Ax = start
        while self.squareAndMultiply(g, Ax, p) != Ay and Ax <= stop + 1:
            Ax += 1;
            
        # Not in range?
        if Ax == stop + 1:
            return "Private key not in range"
        
        # Report shared key
        return "Shared key %d" % self.squareAndMultiply(By, Ax, p)

    @classmethod
    def input(cls):
        # For each prime,primitive-root pair
        for prime, root in itertools.islice(cls.generateRoots(), fi.job.MAX_JOBS):
            # Calculate public keys
            Ay = cls.squareAndMultiply(
                root,
                random.randint(1, prime - 1),
                prime
            )
            By = cls.squareAndMultiply(
                root,
                random.randint(1, prime - 1),
                prime
            )

            # Split up input
            for partition in fi.job.partition(range(1, prime + 1), fi.job.MAX_INSTANCES):
                yield (prime, root, Ay, By, partition[0], partition[-1])

    @classmethod
    def squareAndMultiply(cls, base, power, modulus):
        """
        base:int | power:int | modulus:int -> int

        Purpose self-explanatory. Useful for avoiding integer overflow.
        """
        binary_power = []

        while power > 0:
            binary_power.insert(0, power % 2)
            power /= 2

        output = 1
        for bit in binary_power:
            if bit:
                output = (output * output * base) % modulus
            else:
                output = (output * output) % modulus

        return output
        
    @classmethod
    def generateRoots(cls):
        """
        None -> generator(int, int)

        Generate forever (prime, primitive_root) pairs, where prime >= MIN_MOD
        """
        for mod in itertools.count(cls.MIN_PRIME):
            # Only want primes
            if not cls.isPrime(mod):
                continue

            # Check order of roots up to mod
            factors = cls.factorize(mod - 1)

            if mod >= cls.MIN_MOD:
                for root in range(cls.MIN_PRIME, mod):
                    if cls.isRoot(mod, root, factors):
                        yield mod, root
            
    @classmethod
    def isRoot(cls, mod, root, factors):
        """
        mod:int | root:int | factor:[int] -> bool

        Verifies that 'order' of root % mod is mod - 1 by checking all prime factor periods (root^(p-1)/prime % mod == 1)
        """
        for factor in factors:
            if cls.squareAndMultiply(root, (mod - 1) / factor, mod) == 1:
                return False

        return True

    @classmethod
    def factorize(cls, number):
        """
        number:int -> [int]

        Returns list of prime factors of number (sans exponents)
        """
        factors = []

        for prime in cls.primes:
            if prime > number:
                break

            if number % prime == 0:
                factors.append(prime)

        return factors
        
    @classmethod
    def isPrime(cls, number):
        """
        number:int -> bool

        IMPORTANT: for this to work, you must access the primes in order (2, 3, 5, ..) because it builds the list as it goes.
        """

        if cls.primes and number < cls.primes[-1]:
            return number in cls.primes

        for prime in cls.primes:
            if number % prime == 0:
                return False

        cls.primes.append(number)
        return True

class Tasker(pb.Root):
    TASKS = {
        'DiffieHellman': DiffieHellman
    }
    
    def remote_getTask(self, task):
        return self.TASKS[task]()

def gotTasker(tasker):
    tasker.callRemote("getTask", "diffie_hellman").addCallback(doJob)
    
def doJob(remote_job):
    for i in DiffieHellman.input():
        remote_job.callRemote("getOutput", *i).addCallback(gotOutput)
        
def gotOutput(output):
    print output
        
if __name__ == '__main__':
    if sys.argv[1] == "client":
        print "client"
        factory = pb.PBServerFactory(Tasker())
        reactor.listenTCP(9000, factory)
        reactor.run()
    else:
        print "server"
        factory = pb.PBClientFactory()
        reactor.connectTCP("localhost", 9000, factory)
        factory.getRootObject().addCallback(gotTasker)
        reactor.run()