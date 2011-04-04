from twisted.application import internet, service
from twisted.python import log
from twisted.spread import pb

import fi
import fi.log

import fi.job
import fi.job.controller

import fi.throttle
import fi.throttle.controller

import fi.web
import fi.web.controller

factories = (
    (fi.job.PORT,       pb.PBServerFactory(fi.job.controller.JobServerController())),
    (fi.throttle.PORT,  pb.PBServerFactory(fi.throttle.controller.ThrottleServerController())),
    (fi.web.PORT,       fi.web.controller.WebController()),
)

fi.log.startLogging('server')

if __name__ == '__main__':
    # Python
    from twisted.internet import reactor
    
    for port, factory in factories:
        factory.noisy = False
        reactor.listenTCP(port, factory)
    
    reactor.run()

else:
    # Daemon
    from twisted.application import internet, service
    
    collection = service.IServiceCollection(
        service.Application("FreeInternet Server", uid=1, gid=1)
    )
    
    for port, factory in factories:
        factory.noisy = False
        internet.TCPServer(port, factory).setServiceParent(collection)