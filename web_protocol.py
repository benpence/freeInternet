from twisted.web.resource import Resource
from twisted.web.static import File

class JSONProtocol(Resource):
    def __init__(self, service):
        Resource.__init__(self)
        self.service = service
            
    def render_GET(self, request):
        return self.service.json()

class WebProtocol(Resource):
    def __init__(self, service):
        Resource.__init__(self)
        self.service = service
    
    def getChild(self, name, request):
        # JSON request
        if(name.endswith('.json')):
            return JSONProtocol(self.service)
        else:
            return File('web/').getChild(name, request)