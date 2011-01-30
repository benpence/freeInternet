import sys

from twisted.application import internet, service
from twisted.internet import reactor
from twisted.python import log

import common
from job_controller import JobServerController, JobClientController

_HOST = "127.0.0.1"
_PORT = 5555

class JobServer(object):
    def __init__(self, action, port=_PORT):
        self.application = service.Application('FreeInternet Server', uid=1, gid=1)
    
        factory = JobServerController()
        
        reactor.listenTCP(port, factory)
        
        #internet.TCPServer(_PORT, factory).setServiceParent(
            #service.IServiceCollection(self.application))
        reactor.run()

class JobClient(object):
    _FILE_DIRECTORY = "client_jobs"
    
    def __init__(self, action, host=_HOST, port=_PORT):
        factory = JobClientController()
        factory.file_directory = self._FILE_DIRECTORY
        factory.reactor = reactor
        
    def connect():
        reactor.connectTCP(host, port, factory)
        reactor.run()
        
    def stuff(self):
        """ADD IN FILE CHECKING?"""
        
        # Decompress job and input data
        commands.getoutput('tar xzvf %s' % job_path)
        
        # Run job on input data
        commands.getoutput('%s/job < %s/input > %s/output' %
            tuple(3 * [self._FILE_DIRECTORY]))
        
        # Compress results
        self.filename = common._random_hash()
        self.results_path = "%s/%s" % (self._FILE_DIRECTORY, self.filename)
        
        commands.getoutput('tar cvf %s %s/output' %
            self.results_path,
            self._FILE_DIRECTORY)
        
        # Remove unnecessary files
        commands.getoutput('rm %s/job %s/input %s/output' %
            tuple(3 * [self._FILE_DIRECTORY]))

valid_args = (
    ("module", lambda x: x in ("server", "client")),
    ("action", lambda x: x in ("start", "stop", "status", "restart", "test")),
    ("host",   lambda x: x),
    ("port",   lambda x: common.isNumber(x))
    )

def usage():
    print "Usage: job_application.py [module] [action] (host) (port)"
    exit(0)

if __name__ == "__main__":
    num_args = len(sys.argv)
    # Valid arguments?
    for i in range(1, num_args):
        if not valid_args[i - 1][1](sys.argv[i]):
            usage()

    # For logging
    log.startLogging(sys.stdout)#_file = DailyLogFile("log", "./")
    #application.setComponent(ILogObserver, FileLogObserver(log_file).emit)

    if sys.argv[1] == "server":
        JobServer(*sys.argv[2:])
    elif sys.argv[1] == "client":
        JobClient(*sys.argv[2:])
    else:
        """wtf wTf WTF YOU JUST SAID IT WAS VALID"""
