#!/usr/bin/python

from pyftpdlib import ftpserver
authorizer = ftpserver.DummyAuthorizer()
authorizer.add_user("bmp", "12345", "/home/bmp", perm="elradfmw")
authorizer.add_anonymous("/home/bmp")
handler = ftpserver.FTPHandler
handler.authorizer = authorizer
address = ("127.0.0.1", 21)
ftpd = ftpserver.FTPServer(address, handler)
ftpd.serve_forever()
