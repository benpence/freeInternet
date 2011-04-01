from twisted.application import internet, service
from twisted.python import log
from twisted.spread import pb

import fi

import fi.job
import fi.job.controller

import fi.throttle
import fi.throttle.controller

factories = (
    (fi.job.PORT,       fi.job.controller.JobClientController()),
    (fi.throttle.PORT,  fi.throttle.controller.ThrottleClientController()),
)

application = service.Application("FreeInternet Client", uid=0, gid=0)

for port, factory in factories:
    client = internet.TCPClient(fi.HOST, port, factory)
    client.setServiceParent(
        service.IServiceCollection(application)
    )
    
    print "Added"