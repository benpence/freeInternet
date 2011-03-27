from twisted.internet import utils

import exception

class Shell(object):
    def __init__(self, *commands):
        self.commands = []
        
        for command in commands:
            self.add(*command)
        
        self.index = 0
    
    def _dummyAction(self, data):
        pass
    
    def add(self, command, function=None):
        if function:
            self.commands.append((command, function))
        else:            
            self.commands.append((command, self._dummyAction))
    
    def execute(self):
        def react(data):
            command = self.commands[self.index - 1]
            
            if len(command) is not 2:
                raise exception.UnexpectedError("Invalid tuple in command list")
                
            self.commands[self.index - 1][1](data)

            self.execute()

        if self.index == len(self.commands):
            self.commands = []
            self.transport.loseConnection()

        command = self.commands[self.index][0].split()

        executable = command[0]
        arguments = command[1:]

        d = utils.getProcessOutput(
            executable,
            arguments,
            errortoo=True
        )

        self.index += 1

        d.addCallback(react)
        
        return d