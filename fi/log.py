import sys
import os
import re

from twisted.python import log

import fi

def startLogging(name):
    ClassLogger(sys.stdout).start()
    ClassLogger(
        open(
            os.path.join(fi.ROOT_DIRECTORY, 'logs', name + '.log'),
            'w'
        )
    ).start()
    
class ClassLogger(log.FileLogObserver):
    expression = r'\[.+\]'
    
    def emit(self, logDict):
        if 'system' in logDict and 'message' in logDict:
            # Web
            if 'HTTPChannel' in logDict['system']:
                logDict['system'] = 'WebController'
            
            # Check for [Class] in message
            else:
                message = ' '.join(logDict['message'])
                match = re.match(self.expression, message)
            
                if match:
                    logDict['system'] = match.group()[1:-1]
                    logDict['message'] = (message.replace(
                        match.group() + ' ',
                        ''
                        ),
                    )
        
        # Now log normally
        log.FileLogObserver.emit(self, logDict)