import commands
import subprocess
import sys

import protocols
import client_class

# Start up server
process = subprocess.Popen("python server_class.py",
                            shell=True,
                            stdout=sys.stdout)
#while "LOG" not in process.stdout.read():
    #pass

cli = client_class.Client()

# Test file protocol
print commands.getoutput("mkdir serverFiles clientFiles")
print commands.getoutput("echo 'unit test' > serverFiles/123")
print commands.getoutput("echo 'unit test' > clientFiles/123")

cli.connect("file", protocols.ProtocolFile._JOB_NEW, directory="helper/clientFiles")
cli.connect("file", protocols.ProtocolFile._JOB_OLD, directory="helper/clientFiles", jobID=123)
commands.getoutput("rm -r serverFiles clientFiles")

# Test echo protocol
cli.connect("echo", protocols.ProtocolEcho._FROM_CLIENT)
cli.connect("echo", protocols.ProtocolEcho._FROM_SERVER)

# Test message protocol
notes = ["testing", "testing", "1", "2", "3"]
cli.connect("message", protocols.ProtocolMessage._FROM_CLIENT, messages=notes)
