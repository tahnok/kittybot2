import rss
import commands
import re

class flickr(commands.Command):

    def __init__(self):
        self.tagre = re.compile('!tag (\\w+)')
        self.kittyre = re.compile('!kitty')
        self.kittensre = re.compile('!KITTENS')

    def execute(self, message, sender=None, conncetion=None):
        if self.kittyre.match(message):
            return flickr('kitty')
        m = self.regex.match(message)
        if m is not None:
            return flickr(m.group(1))

    def flickr(tag):
        rickroll = False
        if random.randint(0,9) == 9:
            rickroll = True
        return getitem("http://api.flickr.com/services/feeds/photos_public.gne?tags=%s&lang=en-us&format=rss_200" % tag, rickroll)
