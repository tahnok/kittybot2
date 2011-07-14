import os
import glob

class Command:
    """Class representing an irc command. Must implement execute which returns a tuple. If the command matches it returns the resulting string, otherwise it returns None. Alternatively you can used the connection object to send private messages or other information"""

    def execute(self, message, sender=None, connection=None):
        return None


registered = []

dirList = glob.glob('./commands/*.py')

for path in dirList:
    cFile = path.split("/")
    x = cFile[2].split(".")
    __import__("commands." + x[0])
    

unreachable = "Feed unreachable. Sorry :S"
