from sys import exit, stderr
try:
    from .Server import Server
except SystemError:
    stderr.write("Monopoly.Server [ERROR]: Server must be run as a module. Check the README for instructions")
    exit(1)

"""
Allows for running the code using python3 -m Server
"""

# Set up a Server instance
server = Server()

# Allow for Keyboard interrupts
try:
    server.serve()
except KeyboardInterrupt:
    server.close()

