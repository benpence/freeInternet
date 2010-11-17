#!/usr/bin/python

from pyftpdlib import ftpserver
authorizer = ftpserver.DummyAuthorizer()
authorizer.add_user("ben", "12345", "/home/ben", perm="elradfmw")
authorizer.add_anonymous("/home/ben")
handler = ftpserver.FTPHandler
handler.authorizer = authorizer
address = ("127.0.0.1", 21)
ftpd = ftpserver.FTPServer(address, handler)
ftpd.serve_forever()
