from sys import exit, stderr
from argparse import ArgumentParser
try:
    from .main import Main
except SystemError:
    stderr.write("Monopoly.Client [ERROR]: Client must be run as a module. Check the README for instructions")
    exit(1)

"""
Allows for running the code using python3 -m Client
"""

parser = ArgumentParser(
    prog="Monopoly.Client",
    usage="python3 -m Client [-h] [-c|-j|--poll] [-h host] [-n username] [-p password]",
    description="%(prog)s: Client of the Monopoly game written by Super Confused"
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-c', '--create',
    help='Create a game',
    action='store_true',
)
group.add_argument(
    '-j', '--join',
    help='Join a game',
    action='store_true',
)
group.add_argument(
    '--poll',
    help='Poll the network for open games',
    action='store_true'
)
parser.add_argument(
    '--host',
    help='Specify the host. Defaults to localhost',
    default='',
    action='store',
)
parser.add_argument(
    '-n', '--name',
    help='Specify your username',
    default='Guest',
    action='store',
)
parser.add_argument(
    '-p', '--password',
    help='Specify the password',
    default=None,
    action='store',
)

# Set up a the Client Stuff
args = parser.parse_args()
gui = Main()
if args.create:
    gui.create(args.host, args.name, args.password)
elif args.join:
    gui.join(args.host, args.name, args.password)
elif args.poll:
    print("Polling the network for games")
    servers = gui.poll()
    if not servers:
        print("No Servers running")
    else:
        for server in servers:
            print(server)
    exit(0)
else:
    print("You must specify to create, join or poll. Try the -h option")
    exit(1)
# Now run the game
gui.init_display()
gui.run()