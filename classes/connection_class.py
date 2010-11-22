#!/usr/bin/python

import logging #Logger class

class Connection(object):
    """
    Connection(output= # print logs to stdout?)
    """

    __instances = {}
    count = 0

    def __init__(self, output=True):
        self.output = output

        self.running = True # for threading
        self.sock = None # socket

        self.id = Connection.count # identifier for logging
        Connection.count += 1
        Connection.__instances[self.id] = self # singleton

    def log(self, *args, **kargs):
        # If not specified, go by the object's default value for visualCue (output)
        if 'visualCue' not in kargs:
            kargs['visualCue'] = self.output

        logging.Logger.log(*args, **kargs)

if __name__ == "__main__":
    hey = Connection()
    hey.log("program",
            "THIS IS A TEST",
            visualCue=True)
