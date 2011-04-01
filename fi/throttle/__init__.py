import fi
import os

PORT = 6666
VPN_INTERFACE = "tun0"
VPN_SERVER_IP = "10.8.0.1" # VPN address of server

AVAILABLE_BANDWIDTH = 4000 # Initial maximum bandwidth
BANDWIDTH_HEURISTIC = 18 # For adjustment to real units

PATHLOAD_DIRECTORY = os.path.join(fi.ROOT_DIRECTORY, 'fi', 'throttle', 'pathload') 
PATHLOAD_CLIENT = "128.164.160.197" # The client to use for pathload
