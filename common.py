import random
random.seed()

_DATABASE_PATH = "freeinternet.db"
_SERVER_DIRECTORY = "server_files"
_CLIENT_DIRECTORY = "client_files"

_MAX_JOBS = 100
_MAX_INSTANCES = 3

def random_hash():
    """
    None -> str
    """
    
    return "%016x" % random.getrandbits(128)
    
def isNumber(number):
    try:
        float(number)
        return True
    except ValueError:
        return False
