import random
import urllib2
from bs4 import BeautifulSoup

class Annoy():
	def __init__(self, input, output):
		self.input = input
		self.output = output


	def generate_config(self, filename):
		f = open("annoy.txt", "r")
		o = open("annoy.cfg", "w")

		jokes = []
		for line in f:
		    if len(line.strip()) > 127:
		        print "Warning: Joke length exceeds max Dota 2 character limit by {} characters. It will be truncated.".format(len(line.strip()) - 127)
		    else:
		        jokes.append(line.strip())

		f.close()
		random.shuffle(jokes)

		i=0
		for joke in jokes:
		    o.write("alias ran_say{}\t\"say {}; ran_move\"\n".format(i, joke.replace('"', "'")))
		    i += 1
		i -= 1

		o.write("\n\n")

		for x in range(i-1):
		    o.write("alias ran_move{}\t\"alias ran_say ran_say{}; alias ran_move ran_move{}\"\n".format(x, x+1, x+1))

		o.write("alias ran_move{}\t\"alias ran_say ran_say0; alias ran_move ran_move0\"\n".format(i))

		o.write("\n\nalias ran_say ran_say0\nalias ran_move ran_move0\n\nbind o ran_move\nbind p ran_say\n\nbind mouse1 ran_move\n\nbind mouse2 ran_move\n\n")

		o.write("bind i \"say It's a script that downloads jokes from Sickipedia.\"")

		o.close()


	def sickipedia_random(self):
		o = open("annoy.txt", "w")
		for i in range(10):
		    downloaded_data  = urllib2.urlopen('http://www.sickipedia.org/random')

		    parsed_html = BeautifulSoup(downloaded_data.read())
		    s = parsed_html.body.find('section', attrs={'class':'jokeText'}).text.strip().split("\n")
		    if len(s) == 3:
		        o.write("{} {}\n".format(s[0], s[2]))

		o.close()

	def sickipedia_top_100(self):
		downloaded_data  = urllib2.urlopen('http://www.sickipedia.org/feeds/?1262778980.xml')

		soup = BeautifulSoup(downloaded_data.read())

		o = open("annoy.txt", "w")
		for joke in soup.find_all("description"):
		    if joke.string == None:
		        continue
		    joke = joke.string.replace("<br/><br/>", " ").replace("<br/>", "").encode('ascii', 'ignore')
		    o.write("{} \n".format(joke))

		o.close()


	def anti_joke_random(self):
		o = open("annoy.txt", "w")
		for i in range(5):
		    downloaded_data  = urllib2.urlopen('http://anti-joke.com/random/anti-joke')

		    parsed_html = BeautifulSoup(downloaded_data.read())
		    s = parsed_html.body.find_all('h3', attrs={'class':'content'})
		    st = ""
		    for thing in s:
		        st += thing.text.replace("\n", "//nextjokelol//").encode("ascii", "ignore")
		    st = st.replace(chr(13), " ")
		    st = st.replace("//nextjokelol//", "\n")[1:]
		    o.write(st + "\n")

		o.close()

	def default_puns(self):
		o = open("annoy.txt", "w")
		i = open("default.txt", "r")
		for line in i:
			o.write(line)
		o.close()
		i.close()
