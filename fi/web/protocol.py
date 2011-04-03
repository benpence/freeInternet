import os

from twisted.web.resource import Resource
from twisted.web.static import File

import fi

class JSONProtocol(Resource):
    def __init__(self, service, name):
        Resource.__init__(self)
        self.service = service
        self.name = name
            
    def render_GET(self, request):
        return self.service.json(request, self.name)

class WebProtocol(Resource):
    def __init__(self, service):
        Resource.__init__(self)
        self.service = service
    
    def getChild(self, name, request):
        # JSON request
        if(name.endswith('.json')):
            return JSONProtocol(self.service, name)
            
        # Static file serving
        else:
            return File(
                os.path.join(
                    fi.ROOT_DIRECTORY,
                    'fi',
                    'web'
                )
            ).getChild(name, request)