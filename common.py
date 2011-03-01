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


try:
    import sqlite3 as sqlite
except ImportError, e:
    import sqlite
    print "'import sqlite3' failed. Using sqlite"

class db_connection(object):
    """
    Makes database connections easier
    """
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.db = sqlite.connect(self.path)
        self.cursor = self.db.cursor()
        return (self.db, self.cursor)

    def __exit__(self, type, value, traceback):
        self.db.commit()
        self.db.close()


from twisted.internet import utils, defer

class Shell(object):
    def __init__(self):
        self.callStack = defer.succeed("")
    
    def execute(self, shell_command, react_function=None):
        """
        shell_command:str | react_function:lambda -> None
        
        Original Deferred -> Shell deferred  Shell deferred    ...
                             |              /  |              /
                             V             /   V             /
                             react_function    react_function
        """

        def react(output):
            if react_function:
                react_function(output)
    
        words = shell_command.split()

        executable = words[0]
        arguments = words[1:]

        self.callStack.addCallback(
            lambda s: utils.getProcessOutput(
                executable,
                arguments,
                errortoo=True
            ).addCallback(react))
