import random
random.seed()

def random_hash():
    """
    None -> str
    """
    
    return "%016x" % random.getrandbits(128)
    
def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False