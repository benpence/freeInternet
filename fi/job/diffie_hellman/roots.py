import math
import itertools

# Constants
MIN_PRIME = 2 # First prime is 2. DON'T CHANGE THIS
MIN_MOD = 2000 # Start giving moduli at this number and above

# Globals
primes = []

def squareAndMultiply(base, power, modulus):
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

def isPrime(number):
    """
    number:int -> bool
    
    IMPORTANT: for this to work, you must access the primes in order (2, 3, 5, ..) because it builds the list as it goes.
    """
    
    if primes and number < primes[-1]:
        return number in primes
    
    for prime in primes:
        if number % prime is 0:
            return False
    
    primes.append(number)
    return True

def factorize(number):
    """
    number:int -> [int]
    
    Returns list of prime factors of number (sans exponents)
    """
    factors = []

    for prime in primes:
        if prime > number:
            break
        
        if number % prime is 0:
            factors.append(prime)

    return tuple(factors)

def isRoot(mod, root, factors):
    """
    mod:int | root:int | factor:[int] -> bool
    
    Verifies that 'order' of root % mod is mod - 1 by checking all prime factor periods (root^(p-1)/prime % mod == 1)
    """
    for factor in factors:
        if squareAndMultiply(root, (mod - 1) / factor, mod) is 1:
            return False
    
    return True

def generateRoots():
    """
    None -> generator(int, int)
    
    Generate forever (prime, primitive_root) pairs, where prime >= MIN_MOD
    """
    for mod in itertools.count(MIN_PRIME):
        # Only want primes
        if not isPrime(mod):
            continue

        # Check order of roots up to mod
        factors = factorize(mod - 1)

        if mod >= MIN_MOD:
            for root in range(MIN_PRIME, mod):
                if isRoot(mod, root, factors):
                    yield mod, root

def test():
    trues = []
    for mod, root in itertools.islice(generateRoots(), 100):
        for i in range(1, mod):
            if squareAndMultiply(root, i, mod) is 1 and i != mod - 1:
                print mod, root, i
    
    trues = []
    for mod, root in itertools.islice(generateRoots(), 100):
        for i in range(1, mod - 1):
            if squareAndMultiply(root, i, mod) is 1:
                print mod, root, i
    
if __name__ == '__main__':
    test()