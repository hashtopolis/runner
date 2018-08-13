import os

from htpserver.HTService import HTService

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    service = HTService('HTService', pid_dir='/tmp', working_directory=os.getcwd())

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        try:
            service.stop()
        except ValueError as e:
            print("Could not stop service: " + str(e))
    elif cmd == 'status':
        if service.is_running():
            print("Service is running.")
        else:
            print("Service is not running.")
    else:
        sys.exit('Unknown command "%s".' % cmd)
