"""Going to contain all my useful rss methods, like rick roll, get item, etc..."""

import feedparser
import urlshortener
import random

def getitem(url, rickroll):
    feed = feedparser.parse(url)
    if len(feed) == 0:
        return "Empty or broken feed. Sorry :S"

    choice = random.randint(0, len(feed)-1)
    toreturn = "%s " % feed['entries'][choice]['title']
    if rickroll:
        #rickroll
        toreturn = toreturn + urlshortener.shorten("http://www.youtube.com/watch?v=oHg5SJYRHA0")
    else:
        toreturn = toreturn + urlshortener.shorten(feed['entries'][choice]['link'])
    return removeNonAscii(toreturn)

def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

