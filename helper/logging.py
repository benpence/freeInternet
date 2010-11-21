#!/usr/bin/python

import datetime

class Logger:
    """
    Logger(    program, # App/thread that is logging
            message, # String to log
            messateType=, # Sting values 'LOG' or 'ERR'
            visualCue=) # Print to terminal?

        Generic logging class. log() is a class function.
    """

    logFiles = {}
    visualCues = True

    def log(program, message, messageType="LOG", visualCue=True, continuation=False):
        """
        writes message to respective log file
        """

        log = message
        if not continuation:
            log = "%s %s %s: %s" % (datetime.datetime.now(), messageType, program, message)

        ## Output to file ##
        #Open file if not already open
        if program not in Logger.logFiles:
            Logger.logFiles[program] = open("log_" + program, 'a')

        Logger.logFiles[program].write(log + "\n")

        ## Output to screen ##
        if visualCue and Logger.visualCues:
            print log
    log = staticmethod(log)

    def close():
        for file in Logger.logFiles:
            file.close()
    close = staticmethod(close)
    
# Test
if __name__ == "__main__":
    Logger.log("logger", "testing error", messageType = "ERR", visualCue = True)
    Logger.log("logger", "testing log", messageType = "LOG", visualCue = True)
