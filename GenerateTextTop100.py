import urllib2
from bs4 import BeautifulSoup


downloaded_data  = urllib2.urlopen('http://www.sickipedia.org/feeds/?1262778980.xml')

soup = BeautifulSoup(downloaded_data.read())

o = open("annoy.txt", "w")
for joke in soup.find_all("description"):
    if joke.string == None:
        continue
    joke = joke.string.replace("<br/><br/>", " ").replace("<br/>", "").encode('ascii', 'ignore')
    o.write("{} \n".format(joke))

o.close()
