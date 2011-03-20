from twisted.trial import unittest

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.test import proto_helpers

import shell

class TestSequenceFunctions(from twisted.trial import unittest.TestCase):
    def setUp(self):
        factory = protocol.ServerFactory()
        self.protocol = factory.buildProtocol(
            ('127.0.0.1', 0)
        )
        self.tr = proto_helpers.StringTransport()
        self.protocol.makeConnection(self.tr)

        self.messages = (
            "hey",
            "ho",
            "SUPER"
        )

    def doIt(self, data):
        self.data += data

    """TODO: Figure out where loop is getting stuck"""

    def test_init(self):
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
        )