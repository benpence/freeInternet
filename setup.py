import sys

def uninstall():
    pass

def install():
    pass

def Main(action):
    uninstall()

    if action == "install":
        install()


def usage():
    print "Usage: setup.py {install, uninstall}"
    exit()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()

    if sys.argv[1] not in ["install", "uninstall"]:
        usage()

    Main(sys.argv[1])
