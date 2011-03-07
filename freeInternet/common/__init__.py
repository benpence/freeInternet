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

# Web
_WEB_PORT = 7777

import random
random.seed()

def randomHash():
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