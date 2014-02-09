import random
import urllib2
from bs4 import BeautifulSoup

class Annoy():
	sites = ["sickipedia-random", "sickipedia-top-100", "anti-jokes-random", "anti-jokes-top"]
	inf = ""
	outf = ""

	def __init__(self):
		pass

	def run(self, args):
		if args.input:
			if args.input[-4:] == ".txt":
				print "Warning: input file is not a text file. Are you sure you typed the name right?"
			if os.path.exists(args.input) && !args.download && !args.default:
				self.inf = args.input
			else:
				print "Error: input file does not exist. Exiting..."
				return
		else:
			if os.path.exists("annoy.txt") && !args.download && !args.default:
				self.inf = "annoy.txt"
			else:
				print "Error: annoy.txt does not exist. Exiting..."
				return

		if args.output:
			if args.output[-4:] == ".cfg":
				print "Warning: output file is not a config file. Are you sure you typed the name right?"
			self.outf = args.output

		else:
			self.outf = "annoy.cfg"

		if args.list:
			print "Avoid sites to download jokes from are:"
			print "\n\t".join(sites)
			print "\nJust use 'Dotannoy -d SITE_NAME' to download jokes from that site"
			return

		if args.default:
			default_puns



	def generate_config(self):
		f = open(self.args.INPUT, "r")
		o = open(self.args.OUTPUT, "w")

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
		o.write("alias ran_move{}\t\"alias ran_say ran_say0; alias ran_move ran_move0\"\n\n\n".format(i))

		o.write("alias ran_say ran_say0\n")
		o.write("alias ran_move ran_move0\n\n")
		o.write("bind o ran_move\n")
		o.write("bind p ran_say\n\n")
		o.write("bind mouse1 ran_move\n\n")
		o.write("bind mouse2 ran_move\n\n")

		o.close()


	def sickipedia_random(self):
		o = open(self.input, "w")
		for i in range(10):
		    data  = urllib2.urlopen('http://www.sickipedia.org/random')

		    parsed_html = BeautifulSoup(data.read())
		    s = parsed_html.body.find('section', attrs={'class':'jokeText'}).text.strip().split("\n")
		    if len(s) == 3:
		        o.write("{} {}\n".format(s[0], s[2]))

		o.close()

	def sickipedia_top_100(self):
		o = open(self.input, "w")
		data  = urllib2.urlopen('http://www.sickipedia.org/feeds/?1262778980.xml')

		soup = BeautifulSoup(data.read())

		for joke in soup.find_all("description"):
		    if joke.string == None:
		        continue
		    joke = joke.string.replace("<br/><br/>", " ").replace("<br/>", "").encode('ascii', 'ignore')
		    o.write("{} \n".format(joke))

		o.close()


	def anti_joke_random(self, n):
		o = open(self.input, "w")
		for i in range(n%10+1):
		    data  = urllib2.urlopen('http://anti-joke.com/random/anti-joke')

		    parsed_html = BeautifulSoup(data.read())
		    s = parsed_html.body.find_all('h3', attrs={'class':'content'})
		    st = ""
		    for thing in s:
		        st += thing.text.replace("\n", "//nextjokelol//").encode("ascii", "ignore")
		    st = st.replace(chr(13), " ")
		    st = st.replace("//nextjokelol//", "\n")[1:]
		    o.write(st + "\n")

		o.close()

	def default_puns(self):
		o = open(self.input, "w")
		i = open("default.txt", "r")
		for line in i:
			o.write(line)
		o.close()
		i.close()
