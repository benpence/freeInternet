import socket

# Connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5555))

l = ["hey", "ho", "hiya"]

for i in l:
    sock.send(i)

#sock.close()
