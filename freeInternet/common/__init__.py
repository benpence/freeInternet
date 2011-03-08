# Model
_CHANGES_BEFORE_WRITE = 3 # How many rows changed until write to database

# Job System
_ROOT_DIRECTORY = "/Users/ben/Source/freeInternet"
_DATABASE_PATH = "%s/freeInternet.db" % _ROOT_DIRECTORY
_SERVER_DIRECTORY = "server_files"
_CLIENT_DIRECTORY = "client_files"
_JOB_PORT = 5555
_CHUNK_SIZE = 512

_MAX_JOBS = 100
_MAX_INSTANCES = 3

# General Networking
_HOST = "127.0.0.1"

# Throttle
_THROTTLE_PORT = 6666
_VPN_INTERFACE = "tun0"
_THROTTLE_SLEEP = 2
_IP = "10.8.0.1" # VPN address of server
_MAX_BANDWIDTH = 4000
_BANDWIDTH_HEURISTIC = 18

_PATHLOAD_CLIENT = "128.164.160.197"

# Web
_WEB_PORT = 7777

import random
random.seed()

def randomHash():
    """
    None -> str
    """
    
    return "%x" % random.getrandbits( * 4)
    
def isNumber(number):
    try:
        float(number)
        return True
    except TypeError:
        return False
    except ValueError:
        return False
        
def partition(l, n):
    """
    l:[_] | n:int -> [[_]]
    
    """
    division = len(l) / float(n)
    
    return [
        l[int(round(division * i)): int(round(division * (i + 1)))]
        for i in range(n)
        ]