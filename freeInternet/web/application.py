from twisted.internet import utils

class WebApplication(object):
    @classmethod
    def askBandwidth(cls):
        shell = common_shell.Shell(
            ("")
        )
        shell.execute("", react_function=cls.toldBandwidth)
    
    @classmethod
    def toldBandwidth(cls, bandwidth):
        
        