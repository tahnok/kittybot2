
class Command:
    """Class representing an irc command. Must implement execute which returns a tuple. If the command matches it returns the resulting string, otherwise it returns None. Alternatively you can used the connection object to send private messages or other information"""

    def execute(self, message, sender, connection):
        return None


registered = []

unreachable = "Feed unreachable. Sorry :S"
