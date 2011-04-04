import fi.job.remote

import random
import itertools

class DiffieHellman(fi.job.remote.RemoteJob):
    @classmethod
    def getOutput(cls, p, g, Ay, By, start, stop):
        # Try all stop->stop private keys
        for Ax in range(start, stop + 1):
            product = cls.squareAndMultiply(g, Ax, p)
            
            if product == Ay:
                return "Shared key %d" % cls.squareAndMultiply(By, Ax, p)
                
        return "Private key not in range"
            
        # Report shared key
        return "Shared key %d" % cls.squareAndMultiply(By, Ax, p)
    
    @classmethod
    def squareAndMultiply(cls, base, power, modulus):
        """
        base:int | power:int | modulus:int -> int

        Purpose self-explanatory. Useful for avoiding integer overflow.
        """
        binary_power = []

        while power > 0:
            binary_power.append(power % 2)
            power /= 2
        binary_power.reverse()

        output = 1
        for bit in binary_power:
            if bit:
                output = (output * output * base) % modulus
            else:
                output = (output * output) % modulus

        return output

class DiffieHellmanInput(fi.job.remote.RemoteJobInput):
    # About Task
    DESCRIPTION = "Brute force attack against a Diffie-Hellman-Merkle Key Exchange"
    CREDIT = 5
    INPUT = "(Prime Number, Primitive Root, Public Key 1, Public Key 2, Start Private Key, Stop Private Key)"
    OUTPUT = '("Shared Key #") or ("Private key not in range")'
    
    # Constants
    MIN_PRIME = 2 # First prime is 2. DON'T CHANGE THIS
    MIN_MOD = 2000 # Start giving moduli at this number and above
    INPUT_RANGE = 1000 # How many numbers to check in brute force

    # Globals
    primes = []
        
    @classmethod
    def generateInput(cls):
        # prime, primitive-root pair
        for prime, root in cls.generateRoots():
            # Calculate public keys
            Ay = DiffieHellman.squareAndMultiply(
                root,
                random.randint(1, prime - 1),
                prime
            )
            By = DiffieHellman.squareAndMultiply(
                root,
                random.randint(1, prime - 1),
                prime
            )

            # Split up input
            start = stop = 1
            while start < prime:
                stop = start + cls.INPUT_RANGE
                
                if stop >= prime:
                    stop = prime - 1
                
                yield (prime, root, Ay, By, start, stop)
                
                start += cls.INPUT_RANGE + 1
        
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
    def isRoot(cls, mod, root, factors):
        """
        mod:int | root:int | factor:[int] -> bool

        Verifies that 'order' of root % mod is mod - 1 by checking all prime factor periods (root^(p-1)/prime % mod == 1)
        """
        for factor in factors:
            if DiffieHellman.squareAndMultiply(root, (mod - 1) / factor, mod) == 1:
                return False

        return True
        
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