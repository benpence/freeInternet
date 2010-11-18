#!/usr/bin/python

import sys
import logging #Logger class

_CHUNK_SIZE = 4096

class Connection(object):
    """
    Connection(chunkSize = #, output = boolean)
    """

    __instances = {}
    count = 0

    def __init__(self, chunkSize=_CHUNK_SIZE, output=True):
        self.chunkSize = chunkSize
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

    def pad(self, string):
        while len(string) < self.chunkSize:
            string += "."
        return string


if __name__ == "__main__":
    hey = Connection()
    hey.log("program",
            "THIS IS A TEST",
            visualCue=True)
