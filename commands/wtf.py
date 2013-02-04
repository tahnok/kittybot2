import commands
import re
import rss
import random

class wtf(commands.Command):
    """returns weird freaky shit"""
    def __init__(self):
        self.regex = re.compile('!wtf')

    def execute(self, message, sender, connection):
        if self.regex.match(message):
            return self.wtf()
        else:
            return None

    def wtf(self):
        choices = ['http://strangeweirdporn.com/feed/', 'http://www.scarysextoyfriday.com/feeds/posts/default']
        rickroll = False
        if random.randint(0,9) == 9: 
            rickroll = True
        return rss.getitem(choices[random.randint(0, len(choices) -1)], rickroll)

commands.registered.append(wtf())
