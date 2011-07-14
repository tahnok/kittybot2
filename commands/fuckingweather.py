import urllib
import BeautifulSoup
import commands

class fuckingweather(commands.Command):
    """gets weather from thefuckingweather.com"""

    def execute(self, message, sender, connection):
        args = message.split(" ")
        if args[0] == "!thefuckingweather":
            if len(args) == 1:
                return self.getfuckingweather()
            if len(args) == 2:
                return self.getfuckingweather(args[1])
            if len(args) == 3:
                if args[2] == 'C' or args[2] == 'F':
                    return self.getfuckingweather(args[1], args[2])
        else:
            return None
             
    def getfuckingweather(self, location="montreal", celcius="C"):
        if celcius == "F":
            text = ""
        else:
            text = '&CELSIUS=yes'
        data = urllib.urlopen('http://thefuckingweather.com/?zipcode=%s%s' % (location, text))
        soup = BeautifulSoup.BeautifulSoup(data.read())
        data.close()
        result = soup.find('div', 'large')
        if result is not None:
            return result.contents[0].replace("&deg;", " ") + " " + result.contents[4]
        else:
            return "Oww.. my poor kitty brain"

commands.registered.append(fuckingweather())
