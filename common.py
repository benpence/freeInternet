import random
random.seed()

def _random_hash():
    """
    None -> str
    """
    
    return "%016x" % random.getrandbits(128)