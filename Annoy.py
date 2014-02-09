import random
import urllib2
from bs4 import BeautifulSoup

class Annoy():
	# A list of available sites
	sites = ["sickipedia-random", "sickipedia-top-100", "anti-jokes-random", "anti-jokes-top"]
	# Input and output files
	inf = ""
	outf = ""

	# Default consturcter. Doesn't do anything
	def __init__(self):
		pass


	# Main functions. Handles the arguments and passes to functions that are needed
	def run(self, args):
		# Handle input file argument
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

		# Handle output file argument
		if args.output:
			if args.output[-4:] == ".cfg":
				print "Warning: output file is not a config file. Are you sure you typed the name right?"
			self.outf = args.output
		else:
			self.outf = "annoy.cfg"

		# Handle list argument and return
		if args.list:
			print_sites()
			return

		if args.default:
			default_puns

	# Print a list of avaiable sites to download from
	def print_sites(self):
		print "Avoid sites to download jokes from are:\n\t"
		print "\n\t".join(sites)
		print "\nJust use 'Dotannoy -d SITE_NAME' to download jokes from that site"

	# Generate the file config file
	def generate_config(self, force):
		f = open(self.inf, "r")
		o = open(self.outf, "w")

		# Go through all the lines in the input file, check they're shorter than the
		jokes = []
		i = 0
		for line in f:
		    if len(line.strip()) > 127:
		    	if force:
		    		jokes.append(line.strip()[:127])
		    	else:
		        	print "Warning: Joke on line {} exceeds the Dota 2 character limit by {} characters. It will not be saved.".format(i, len(line.strip()) - 127)
		    else:
		        jokes.append(line.strip())
		    i += 1

		# Shuffle all the jokes
		random.shuffle(jokes)

		# Go through all the jokes and create the say bind for them
		i=0
		for joke in jokes:
		    o.write("alias ran_say{}\t\"say {}; ran_move\"\n".format(i, joke.replace('"', "'")))
		    i += 1
		i -= 1

		o.write("\n\n")

		# Write the randomising alias's for all the say binds
		for x in range(i-1):
		    o.write("alias ran_move{}\t\"alias ran_say ran_say{}; alias ran_move ran_move{}\"\n".format(x, x+1, x+1))
		o.write("alias ran_move{}\t\"alias ran_say ran_say0; alias ran_move ran_move0\"\n\n\n".format(i))

		# Write the rest of the boring config
		o.write("alias ran_say ran_say0\n")
		o.write("alias ran_move ran_move0\n\n")
		o.write("bind o ran_move\n")
		o.write("bind p ran_say\n\n")
		o.write("bind mouse1 ran_move\n\n")
		o.write("bind mouse2 ran_move\n\n")

		o.close()
		f.close()

	# Download random jokes from sickipedia
	def sickipedia_random(self, n):
		o = open(self.inf, "w")

		# Keep loading the random page until we have the required number of random jokes
		for i in range(n):
		    data  = urllib2.urlopen('http://www.sickipedia.org/random')

		    parsed_html = BeautifulSoup(data.read())
		    # Strip the joke from the webpage
		    s = parsed_html.body.find('section', attrs={'class':'jokeText'}).text.strip().split("\n")
		    if len(s) == 3:
		        o.write("{} {}\n".format(s[0], s[2]))

		o.close()

	# Download the top 100 jokes this week from sickipedia
	def sickipedia_top_100(self):
		o = open(self.inf, "w")
		data  = urllib2.urlopen('http://www.sickipedia.org/feeds/?1262778980.xml')

		soup = BeautifulSoup(data.read())

		# Find all the jokes on the page and store them in the input file
		for joke in soup.find_all("description"):
		    if joke.string == None:
		        continue
		    joke = joke.string.replace("<br/><br/>", " ").replace("<br/>", "").encode('ascii', 'ignore')
		    o.write("{} \n".format(joke))

		o.close()

	# Download random jokes from anti-jokes.com
	def anti_joke_random(self, n):
		o = open(self.inf, "w")

		# Download the required number of jokes from the site by scraping the random page
		for i in range(n%12+1):
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

	# Copy the default puns into the text file
	def default_puns(self):
		o = open(self.input, "w")
		i = open("default.txt", "r")
		for line in i:
			o.write(line)
		o.close()
		i.close()
