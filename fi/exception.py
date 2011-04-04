from sqlalchemy.exc import OperationalError

class Error(Exception):
    def __init__(self, value):
        self.value = value
        
    def __strt__(self):
        return repr(self.value)

class UnexpectedError(Error):
    """Input values are not formatted as expected"""
    pass
    
class EmptyQuery(UnexpectedError):
    """Database did not return expected values"""
    pass    