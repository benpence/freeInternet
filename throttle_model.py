import common
import model

class Throttle(model.Model):
    _keys = {
        'ip' :          'VARCHAR',
        }
    _values = {
        'vpn_ip' :      'VARCHAR',
        'credit' :      'INTEGER',
        'bandwidth':    'INTEGER',
        }
    
    @classmethod
    def allocate(cls, allocations):
        """
        allocations:[(str, int)] -> None
        """
        
        ipsToBandwidth = dict(allocations)
        
        for throttle in Throttle.search():
            throttle.bandwidth = ipsToBandwidth[throttle.vpn_ip]
        
def __init__():
    Throttle.readIntoMemory(common._DATABASE_PATH)
    
def __setup__():
    Throttle(
        ip="128.164.160.197",
        vpn_ip="10.8.0.6",
        credit=0,
        )
    Throttle(
        ip="128.164.160.199",
        vpn_ip="10.8.0.10",
        credit=0,
        )
    Throttle.writeToDatabase(common._DATABASE_PATH)

def test():
    Throttle.readIntoMemory(common._DATABASE_PATH)
    throttle = Throttle.search(1)

    print throttle
    throttle.credit += 5
    print throttle

    Throttle.writeToDatabase(common._DATABASE_PATH)


if __name__ == "__main__":
    test()
