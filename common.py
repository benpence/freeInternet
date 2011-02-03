_ROOT_DIRECTORY = "/Users/ben/Source/twisted/"
_SERVER_DIRECTORY = "server_files"
_CLIENT_DIRECTORY = "client_files"

_DATABASE_PATH = "freeInternet.db"
_CHANGES_BEFORE_WRITE = 3 # How many rows changed until write to database

_MAX_JOBS = 100
_MAX_INSTANCES = 3

_HOST = "127.0.0.1"
_PORT = 5555

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
    def __init__():
        self.callStack = defer.succeed("")
    
    def execute(self, shell_command, react_function=None):
        """
        shell_command:str | react_function:lambda -> None
        
        Original Deferred -> Shell deferred  Shell deferred    ...
                             |              /  |              /
                             V             /   V             /
                             react_function    react_function
        """
        
        words = shell_command.split()

        executable = words[0]
        arguments = words[1:]

        def wrapper(last_deferred):
            deferred = utils.getProcessOutput(executable, arguments, errortoo=True)
            
            return deferred
            
        def react(current_deferred):
            if react_function:
                current_deferred.addCallback(react_function)

            return current_deferred
        
        self.callStack.addCallback(wrapper)            
        self.callStack.addCallback(react)