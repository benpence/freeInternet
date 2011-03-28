import fi
import fi.model as model

class Throttle(model.Model):
    ip              = model.Field(model.String, primary_key=True)
    vpn_ip          = model.Field(model.String, primary_key=True)
    credit          = model.Field(model.Integer)
    bandwidth       = model.Field(model.Integer)
    
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
    Throttle(
        ip="128.164.160.197",
        vpn_ip="10.8.0.6",
        credit=1,
        bandwidth=10
    )
    
    Throttle(
        ip="128.164.160.199",
        vpn_ip="10.8.0.10",
        credit=1,
        bandwidth=10
    )
    
    model.commit()
    
model.mapTables()