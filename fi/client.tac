
from twisted.spread import pb

import fi
import fi.job
import fi.job.controller
import fi.throttle
import fi.throttle.controller
import fi.log

fi.log.startLogging('client')

factories = (
    (fi.job.PORT,       fi.job.controller.JobClientController()),
    (fi.throttle.PORT,  fi.throttle.controller.ThrottleClientController()),
)

#Running via python or twistd?
if __name__ == '__main__':
    # Python
    from twisted.internet import reactor
    
    for port, factory in factories:
        reactor.connectTCP(fi.HOST, port, factory)
    
    reactor.run()

else:
    # Twistd
    from twisted.application import internet, service
    
    collection = service.IServiceCollection(
        service.Application(
            "FreeInternet Client",
            uid=1, gid=1
        )
    )
    
    for port, factory in factories:
        internet.TCPClient(fi.HOST, port, factory).setServiceParent(collection)