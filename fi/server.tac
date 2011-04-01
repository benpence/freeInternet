from twisted.application import internet, service
from twisted.python import log
from twisted.spread import pb

import fi

import fi.job
import fi.job.controller

import fi.throttle
import fi.throttle.controller

import fi.web
import fi.web.controller

factories = (
    (fi.job.PORT,       pb.PBServerFactory(fi.job.controller.JobServerController()),
    (fi.throttle.PORT,  pb.PBServerFactory(fi.throttle.controller.ThrottleServerController()),
    (fi.web.PORT,       fi.web.controller.WebController()),
)

application = service.Application("FreeInternet Server", uid=0, gid=0)

for port, factory in factories:
    server = internet.TCPServer(fi.HOST, port, factory)
    server.setServiceParent(
        service.IServiceCollection(application)
    )