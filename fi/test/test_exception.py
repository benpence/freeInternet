from twisted.trial import unittest

from fi import exception

class TestSequenceFunctions(unittest.TestCase):
    
    exceptions = (
        exception.Error,
        exception.UnexpectedError,
        exception.EmptyQuery,
        exception.ConnectionError,
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