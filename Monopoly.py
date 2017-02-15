"""
    Just a script that I'm using to store extra classes / functions for use all across the project
"""


class MonopolyException(BaseException):

    def __init__(self, command, message):
        # Construct a custom message
        msg = "MonopolyException raised by {0}: {1}".format(command, message)
        super(MonopolyException, self).__init__(msg)

        # Store the command that caused the error
        self.command = command