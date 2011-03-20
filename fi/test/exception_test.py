from twisted.trial import unittest

import exception

class TestSequenceFunctions(from twisted.trial import from twisted.trial import unittest.TestCase):
    
    exceptions = (
        exception.Error,
        exception.UnexpectedError,
        exception.EmptyQuery,
        exception.ConnectionError,
        exception.InitializeError
    )
    
    def test_exceptions(self):
        
        def exceptionRaiser(e):
            raise e('TEST TEST')
            
        for e in self.exceptions:
            self.assertRaises(
                e,
                exceptionRaiser,
                e
            )