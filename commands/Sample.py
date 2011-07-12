from command import Command

class Sample(Command):
    a = "sd"
    def execute(self, message, sender, connection):
        return message
