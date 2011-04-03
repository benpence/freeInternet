from twisted.internet import utils

import fi
import fi.exception

class Shell(object):
    def __init__(self, *commands):
        self.commands = []
        self.deferred = None
        
        for command in commands:
            self.add(*command)
        
        self.index = 0
    
    def _dummyAction(self, data):
        pass
    
    def add(self, command, callback=None):
        if callback:
            self.commands.append((command, callback))
        else:            
            self.commands.append((command, self._dummyAction))
    
    def execute(self):
        def react(data):
            command = self.commands[self.index - 1]
            
            if len(command) != 2:
                raise fi.exception.UnexpectedError("Invalid tuple in command list")
                
            self.commands[self.index - 1][1](data)

            self.execute()

        if self.index == len(self.commands):
            self.commands = []
            self.index = 0
            return

        command = self.commands[self.index][0].split()

        executable = command[0]
        arguments = command[1:]

        # We want to return a deferred
        def startExecuting():
            self.deferred = utils.getProcessOutput(
                executable,
                arguments,
                errortoo=True
            )

            self.index += 1

            self.deferred.addCallback(react)
        
        fi.callLater(startExecuting)
        
        return self.deferred