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
print(args)
if args.create:
    # Create a game
    pass
elif args.join:
    # Join a pre-existing game
    pass
elif args.poll:
    # Poll the network for players
    pass
else:
    print("You must specify to create, join or poll. Try the -h option")