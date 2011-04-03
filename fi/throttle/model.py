import fi.model as model
import fi.exception

class Client(model.Model):
    ip              = model.Field(model.String, primary_key=True)
    vpn_ip          = model.Field(model.String, primary_key=True)
    credit          = model.Field(model.Integer)
    bandwidth       = model.Field(model.Integer)
    model.using_options(order_by='-credit')
    
    @classmethod
    def byIP(cls, ip):
        client = cls.get_by(ip=ip)
        
        if not client:
            if ip != '127.0.0.1':
                raise fi.exception.EmptyQueryError("Invalid IP: " + ip)

            return cls(
                ip='127.0.0.1',
                vpn_ip='127.0.0.1',
                credit=1,
                bandwidth=10
            )
        
        return client
    
    @classmethod
    def allocate(cls, allocations):
        """
        allocations:[(str, int)] -> None
        """
        
        ipsToBandwidth = dict(allocations)
        
        for throttle in cls.query.all():
            throttle.bandwidth = ipsToBandwidth[throttle.vpn_ip]

        model.commit()        
    
def setup():
    Client(
        ip="128.164.160.197",
        vpn_ip="10.8.0.6",
        credit=1,
        bandwidth=10
    )
    
    Client(
        ip="128.164.160.199",
        vpn_ip="10.8.0.10",
        credit=1,
        bandwidth=10
    )
    
    model.commit()

model.mapTables()