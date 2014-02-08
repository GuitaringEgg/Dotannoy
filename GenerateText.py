import urllib2
from bs4 import BeautifulSoup

o = open("annoy.txt", "w")
for i in range(10):
    downloaded_data  = urllib2.urlopen('http://www.sickipedia.org/random')

    parsed_html = BeautifulSoup(downloaded_data.read())
    s = parsed_html.body.find('section', attrs={'class':'jokeText'}).text.strip().split("\n")
    if len(s) == 3:
        o.write("{} {}\n".format(s[0], s[2]))

o.close()
