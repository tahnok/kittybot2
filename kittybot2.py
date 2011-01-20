
"""
This is kittybot v2.0, now in Python!
Requires lxml to run (just sudo apt-get install python-lxml

Code is released under a license I have yet to determine

Thanks to Corey Goldberg for the shorten code

HOWTO:
1. set network, channels, nick, name
2. get a developer key from http://www.ipinfodb.com/
3. paste it into the dev_key file as key
4. ???
5. Profit!

TODO: random kitties every hour
TODO: geohash!
"""

import irclib
import re
import socket
from lxml import etree
import urllib
import time
import dev_key
import random
import feedparser
import urlshortener

network = "irc.freenode.net"
port = 6667
channels = ['#mctest']
nick = 'kittybot2'
name = "secretly a goose"


#this is super hacky, find a way to fix it
reply = "Not Set"

# RSS related things
def getitem(url, rickroll):
    feed = feedparser.parse(url)
    choice = random.randint(0, len(feed)-1)
    toreturn = "%s " % feed['entries'][choice]['title']
    if rickroll:
        #rickroll
        toreturn = toreturn + urlshortener.shorten("http://www.youtube.com/watch?v=oHg5SJYRHA0")
    else:
        toreturn = toreturn + urlshortener.shorten(feed['entries'][choice]['link'])
    return toreturn

def flickr(tag):
    rickroll = False
    if random.randint(0,9) == 9:
        rickroll = True
    return getitem("http://api.flickr.com/services/feeds/photos_public.gne?tags=%s&lang=en-us&format=rss_200" % tag, rickroll)

def wtf():
    choices = ['http://strangeweirdporn.com/feed/', 'http://www.scarysextoyfriday.com/feeds/posts/default', 'http://www.efukt.com/rss.php', 'http://fuckeduppornsites.com/feed/']
    rickroll = False
    if random.randint(0,9) == 9:
        rickroll = True    
    return getitem(choices[random.randint(0, len(choices) -1)], rickroll)

def weather():
    montreal_url = "http://www.weatheroffice.gc.ca/rss/city/qc-147_e.xml"
    feed = feedparser.parse(montreal_url)
    result = feed['entries'][1]['title']
    result = result + ". Bitches"
    return result.replace(u'\xb0', ' ')

# IRC related things

def debug(connection, event):
    print('---------Event')
    print("event type: " + event.eventtype())
    print("event target: " + event.target())
    print("event source: " + event.source())
    print("event arguments: " + str(event.arguments()))

def pubmsg(connection, event):
    global reply
    def say(msg):
        connection.privmsg(event.target(), msg)
    message = event.arguments()[0]
    m = re.match('!locate ([\x5b-\x60\x7b-\x7d]|[\\w-]+$)',message)
    if m is not None:
        reply = event.target()
        a = connection.whois([m.group(1)])
    else:
        reply = parse(message)
        if reply != "":
            say(reply)
        
def privmsg(connection, event):
    print("it's a private msg!")

def parse(msg):
    m = re.match('!wtf', msg)
    if m is not None:
        return wtf()
    m = re.match('!kitty', msg)
    if m is not None:
        return flickr('kitty')
    m = re.match('!tag (\\w+)', msg)
    if m is not None:
        return flickr(m.group(1))
    m = re.match('!weather', msg)
    if m is not None:
        return weather()
    return ""

def handlewho(connection, event):
    print("whois handler")
    global reply
    ip = event.arguments()[2]
    m = re.match('\\w+/', ip)
    if m is not None:
        msg = "Error: User has a hostmask"
    else:
        m = re.match('^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$', ip) 
        if m is None:
            ip = socket.gethostbyname(ip)
        root = etree.parse('http://api.ipinfodb.com/v2/ip_query.php?key=' + dev_key.ipinfodbkey + '&ip=' + ip + '&timezone=false').getroot()
        lon = root.find("Longitude").text
        lat = root.find("Latitude").text
        city = root.find("City").text
        long_url = "http://maps.google.com/maps?f=d&source=s_d&saddr=%s,%s" % (lat, lon)
        short_url = urlshortener.shorten(long_url)
        msg = "City: %s. Map: %s" % (city, short_url)
    connection.privmsg(reply, msg)

def main ():
    irc = irclib.IRC()
    irc.add_global_handler('privmsg', privmsg)
    irc.add_global_handler('pubmsg', pubmsg)
    irc.add_global_handler('whoisuser', handlewho)
    server = irc.server()
    server.connect(network, port, nick, ircname=name)
    for channel in channels:
        server.join(channel)
        server.privmsg(channel, flickr('kitty'))
    irc.process_forever()


if __name__ == '__main__':
    main()



