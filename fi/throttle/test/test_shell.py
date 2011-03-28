from twisted.trial import unittest

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver
from twisted.test import proto_helpers

from fi.throttle import shell
        
class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        factory = protocol.ServerFactory()
        factory.protocol = LineReceiver
        
        self.tr = proto_helpers.StringTransport()
        
        self.protocol = factory.buildProtocol(
            ('127.0.0.1', 0)
        )
        self.protocol.makeConnection(self.tr)

        self.messages = (
            "hey",
            "ho",
            "SUPER"
        )
        self.data = ""

    def doIt(self, data):
        self.data += data

    def assertion(self, data):
        assertEqual(
            self.data,
            ''.join(self.messages)
        )

    """TODO: Get this testing properly"""

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
        
        # Make the assertion the last step
        sh.add(
            'echo "e"',
            function=self.assertion
        )
        
        return sh.execute()
                
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

        sh.add(
            'echo',
            function=self.assertion
        )

        return sh.execute()