import random
random.seed()

_ROOT_DIRECTORY = "/User/ben/Source/twisted/"
_SERVER_DIRECTORY = "server_files"
_CLIENT_DIRECTORY = "client_files"

_DATABASE_PATH = "freeinternet.db"

_MAX_JOBS = 100
_MAX_INSTANCES = 3

_HOST = "127.0.0.1"
_PORT = 5555

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
