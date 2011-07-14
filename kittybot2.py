"""
This is kittybot v2.0, now in Python!

Code is released under GPLv3. See the file named copying for more details

TODO: random kitties every hour
TODO: geohash!
TODO: fix weather to take farhenhite
TODO: mouthpiece mode
"""

import irclib
import re
import socket
from lxml import etree
import urllib
import time
from config import *
import random
import feedparser
import urlshortener
import BeautifulSoup

import commands


halp = """you can try !weather, !thefuckingweather, !wtf, !kitty, !tag [tag name for flickr], !locate [username]. Check out my source code at https://github.com/tahnok/kittybot2"""

#regexes
locatere = re.compile('!locate ([\x5b-\x60\x7b-\x7d]|[\\w-]+$)')

#this is super hacky, find a way to fix it
reply = "Not Set"


def parse(msg, sender, connection):
    for command in commands.registered:
        result = command.execute(msg, sender, connection)
        if result is not None:
            return result
    return None

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
    #This is where the parsing / magic happens
    message = event.arguments()[0]
    m = locatere.match(message)
    if m is not None:
        print "locating..."
        reply = event.target()
        a = connection.whois([m.group(1)])
    elif message == "!halp":
        connection.privmsg(irclib.nm_to_n(event.source()), halp)
    elif message == "!kthxbai":
        print "bai"
        if event.source() == owner:
            say("going to sleep now")
            say("bai")
            connection.quit()
            exit()
        else:
            say("har har nice try")
    else:
        reply = parse(message, event.source(), connection)
        if reply is not None:
            say(reply)
        
def privmsg(connection, event):
    print("it's a private msg!")
    connection.privmsg(event.target, parse(event.arguments()[0]))

def bounce(connection, event):
    connection.join(event.target())

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
        root = etree.parse('http://api.ipinfodb.com/v2/ip_query.php?key=' + ipinfodbkey + '&ip=' + ip + '&timezone=false').getroot()
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
    irc.add_global_handler('kick', bounce)
    server = irc.server()
    server.connect(network, port, nick, ircname=name)
    if freenode:
        server.privmsg("NickServ", "identify " + nickservpwd)
    for channel in channels:
        server.join(channel)
    irc.process_forever()


if __name__ == '__main__':
    main()
