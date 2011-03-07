from twisted.internet import utils

class Shell(object):
    def __init__(self, *commands):
        self.commands = commands
        
        self.index = 0
    
    def _dummyAction(self, data):
        pass
    
    def add(self, command, function=None):
        if function:
            self.commands.append((command, self._dummyAction))
        else:
            self.commands.append((command, function))
    
    def execute(self):
        def react(data):
            command = self.commands[self.index - 1]
            
            if len(command) is not 2:
                
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

def test():
    from twisted.internet import reactor
    
    def doIt(data):
        print data
        
    shell = Shell(
        ("echo 'aaa'", doIt),
        ("echo 'eee'", doIt),
        ("echo 'iii'", doIt),
        ("sleep 3", doIt),
        ("echo 'uuu'", doIt),
    )
    
    shell.execute()
    
    reactor.run()

if __name__ == '__main__':
    test()