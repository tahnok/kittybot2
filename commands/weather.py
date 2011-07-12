import feedparser
import commands

class weather(commands.Command):
    """returns the current weather in montreal"""

    def __init__(self):
        """override if desired"""

    def execute(self, message, sender, connection):
        montreal_url = "http://www.weatheroffice.gc.ca/rss/city/qc-147_e.xml"
        feed = feedparser.parse(montreal_url)
        if len(feed['entries']) == 0:
            return commands.unreachable
        result = feed['entries'][1]['title']
        result = result + ". Bitches"
        return result.replace(u'\xb0', ' ')

commands.registered.append(weather())
