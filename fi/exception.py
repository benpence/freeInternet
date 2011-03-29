class Error(Exception):
    def __init__(self, value):
        self.value = value
        
    def __strt__(self):
        return repr(self.value)

class UnexpectedError(Error):
    pass
    
class EmptyQuery(UnexpectedError):
    pass    
        
class ConnectionError(Error):
    pass