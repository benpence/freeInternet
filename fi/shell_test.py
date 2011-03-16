import unittest

from twisted.internet import reactor

import shell

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.data = ""

        self.messages = (
            "hey",
            "ho",
            "SUPER"
        )

    def doIt(self, data):
        self.data += data

    """TODO: Figure out where loop is getting stuck"""

    """def test_init(self):
        sh = shell.Shell(
            *(
                (
                'echo "%s"' % message,
                lambda data: self.doIt(data)
                )
            for message in self.messages
            )
        )
        
        def thingy(data):
            print "init DONE"
            reactor.stop()
        
        sh.add(
            'echo "e"',
            function=thingy
        )
        
        sh.execute()
        reactor.run()
        
        # After reactor.stop
        assertEqual(
            self.data,
            ''.join(self.messages)
        )
        
    def test_add(self):
        self.messages = (
            "hey",
            "ho",
            "SUPER"
        )

        sh = shell.Shell()

        for message in self.messages:
            sh.add(
                'echo "%s"' % message,
                function=lambda data: self.doIt(data)
            )

        def thingy(data):
            print "add DONE"
            reactor.stop()

        sh.add(
            'echo',
            function=thingy
        )

        sh.execute()
        reactor.run()

        # After reactor.stop
        assertEqual(
            self.data,
            ''.join(self.messages)
        )"""

if __name__ == '__main__':
    unittest.main()