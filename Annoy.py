import random
import urllib2
import wikipedia
import os
import json
import winpaths
import logging as log
from bs4 import BeautifulSoup

class Annoy():
	# A list of available sites
	sites = ["sickipedia-random", "sickipedia-top-100", "anti-jokes-random", "wikipedia-random"]
	# Input and output files
	inf = ""
	outf = ""
	# config settings
	config = None

	# Default constructor. Doesn't do anything
	def __init__(self):
		pass

	# Main functions. Handles the arguments and passes to functions that are needed
	def run(self, args):
		# Set logging level
		if args.verbose:
		    log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
		    log.info("Verbose output.")
		else:
		    log.basicConfig(format="%(levelname)s: %(message)s")

		# load the config file
		self.load_config()


		# make sure we know where the dota config folder is
		if args.steamapps:
			if not self.check_steamapps(args):
				return 1
			else:
				print "Successfully set the steamapps location to '{}'".format(self.config["steamapps"])
				return 0
		else:
			if not self.find_steamapps():
				log.error("Could not find steam install. Please specify the location using 'dotannoy -s STEAMAPPS")
				return 1


		# Handle input file argument
		if args.input:
			if args.input[-4:] == ".txt":
				log.warning("input file is not a text file. Are you sure you typed the name right?")
			if os.path.exists(args.input) and not args.download and not args.default_puns:
				self.inf = args.input
			else:
				log.error("input file does not exist. Exiting...")
				return 1
		else:
			if os.path.exists("annoy.txt") or args.download or args.default_puns:
				self.inf = "annoy.txt"
			else:
				log.error("annoy.txt does not exist. Exiting...")
				return 1


		# Handle output file argument
		if args.output:
			if args.output[-4:] == ".cfg":
				log.warning("output file is not a config file. Are you sure you typed the name right?")
			self.outf = args.output
		else:
			self.outf = "annoy.cfg"


		# Handle list argument and return
		if args.list:
			self.print_sites()
			return


		# Load in the default puns if we need them
		if args.default_puns:
			self.default_puns()


		# Find the site to download puns from if we need to
		if not args.default_puns and args.download:
			if args.download == self.sites[0]:
				self.sickipedia_random(100)
			elif args.download == self.sites[1]:
				self.sickipedia_top_100()
			elif args.download == self.sites[2]:
				self.anti_joke_random(100)
			elif args.download == self.sites[3]:
				self.wikipedia_random(100)
			else:
				log.error("Unknown site {}. Can't download anything.\n\tUse 'Dotannoy -l' to see a list of available sites.".format(args.download))
				return 1


		# Generate the config file
		if not self.generate_config(args):
			return 1


		# Append to autoexec if needed
		if args.autoexec:
			self.append_autoexec()

		return 0

	# Check that the passed steamapps is valid
	def check_steamapps(self, args):
		# path from steamapps to the dota config folder
		dota_path = "common\\dota 2 beta\\dota\\cfg"

		# make sure the given steamapps location is correct
		if os.path.exists(args.steamapps):
			if args.steamapps.find(dota_path) != -1:
				os.chdir(args.steamapps)
				self.config["steamapps"] = os.getpath()
				self.save_config()
				return True
			elif args.steamapps.lower().rfind("steamapps") != -1:
				if os.path.exists(os.path.join(args.steamapps, dota_path)):
					self.config["steamapps"] = os.path.join(args.steamapps, dota_path)
					os.chdir(os.path.join(args.steamapps, dota_path))
					self.save_config()
					return True
		else:
			log.error("Steamapps path given does not exist.")
			return False

		log.error("Steamapps location didn't seem to contain the Dota 2 install.")
		return False

	# Try to find the steamapps folder from program files or the config file
	def find_steamapps(self):
		# default dota path
		dota_path = "\\steamapps\\common\\dota 2 beta\\dota\\cfg"

		# if we are already in the config folder, save the location and continue
		if os.getcwd().find("SteamApps\\common\\dota 2 beta\\dota\\config") != -1:
			self.config["steamapps"] = os.getcwd()
			self.save_config()
			return True

		log.info("Current path {} is not a valid dota install".format(os.getcwd()))

		# if the config folder already has the location, change into the directory
		if self.config["steamapps"]:
			os.chdir(self.config["steamapps"])
			self.save_config()
			return True

		log.info("Config file didn't contain a steamapps folder location")

		# if we can't find it, try and file the steam folder in program files, the default install location
		if os.path.exists(os.path.expandvars("%PROGRAMFILES%") + "\\steam\\" + dota_path):
			self.config["steamapps"] = os.path.expandvars("%PROGRAMFILES%") + "\\steam\\" + dota_path
			self.save_config()
			os.chdir(os.path.expandvars("%PROGRAMFILES%") + "\\steam\\" + dota_path)
			return True

		return False

	# Print a list of available sites to download from
	def print_sites(self):
		print "Avoid sites to download jokes from are:\n\t" + "\n\t".join(self.sites)
		print "\nJust use 'Dotannoy -d SITE_NAME' to download jokes from that site"

	# Generate the file config file
	def generate_config(self, args):
		if not os.path.exists(self.inf):
			log.error("Annoy.txt doesn't exist in Dota's cfg folder.")
			return False

		f = open(self.inf, "r")
		o = open(self.outf, "w")

		# Go through all the lines in the input file, check they're shorter than the
		jokes = []
		i = 0
		for line in f:
		    if len(line.strip()) > 127:
		    	if args.force:
		    		jokes.append(line.strip()[:127])
		    	else:
		        	log.warning("Joke on line {} exceeds the Dota 2 character limit by {} characters.".format(i, len(line.strip()) - 127))
		    else:
		        jokes.append(line.strip())
		    i += 1

		# if the file didn't contain any lines, return an error
		if len(jokes) == 0:
			log.error("Input file doesn't seem to contain any lines. Please make sure {} contains text.".format(self.inf))
			return False

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
		if args.ran_key:
			o.write("bind {} ran_move\n".format(args.ran_key))
		o.write("bind {} ran_say\n\n".format(args.say_key))
		o.write("bind mouse1 ran_move\n")
		o.write("bind mouse2 ran_move\n\n")

		o.close()
		f.close()

		return True

	# Append the exec of this config to the file
	def append_autoexec(self):
		# if autoexec.cfg doesn't exist, create it and write the exec call to it
		# otherwise check if it is already executing annoy.cfg, otherwise append
		# to the end of the file
		if not os.path.exists("autoexec.cfg"):
			o = open("autoexec.cfg", "w")
			o.write("exec {}\n".format(self.outf))
			o.close()
		else:
			o = open("autoexec.cfg", "a+")
			for line in o:
				if line.find("exec {}".format(self.outf)) != -1:
					o.close()
					return
			o.write("exec {}\n".format(self.outf))
			o.close()

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

	# Download top jokes from anti-jokes.com
	def anti_joke_top(self):
		pass

	# Download random articles from wikipedia
	def wikipedia_random(self, n):
		print "Downloading pages from Wikipedia. This may take a moment..."
		f = open(self.inf, "w")
		pages = []

		# get a list of random wikipedia pages.
		# wikipedia.random can only get 10 at a time, so call it so many times
		for x in range(n/10):
			pages += (wikipedia.random(10))
		if n%10 > 0:
			pages += (wikipedia.random(n%10))
		log.info("Found {} random wikipedia pages".format(len(pages)))

		# get the summary info from all the pages.
		# this is a lot of pages, so can take some time
		for page in pages:
			info = None
			try:
				info = wikipedia.page(page)

			# if the request threw a disambiguation error, try to get the first suggestion
			# if that files, just give up on that request. we didn't want it that much anyway
			except wikipedia.exceptions.DisambiguationError as e:
				try:
					info = wikipedia.page(e.options[0])
				except wikipedia.exceptions.DisambiguationError as e:
					continue
				except wikipedia.exceptions.HTTPTimeoutError:
					continue
			except wikipedia.exceptions.HTTPTimeoutError:
				continue

			# save the summary. if it exceeds 127 characters, try to truncate by the first sentence end.
			# if that fails, write it anyway, but it will give warning when it generates the config
			s = info.summary.encode("ascii", "ignore").replace("\n", " ")
			if len(s) < 127:
				log.info("Wrote line with no edits")
				f.write(s + "\n")
			else:
				if s[:127].rfind(". ") != -1:
					f.write(s[:s[:127].rfind(". ")]+1] + "\n")
					log.info("Summary too long, but was truncated")
				else:
					f.write(s + "\n")
					log.info("Summary too long and couldn't truncate")
		f.close()

	# Copy the default puns into the text file
	def default_puns(self):
		# copy default.txt to annoy.txt
		o = open(self.inf, "w")
		i = open("default.txt", "r")
		for line in i:
			o.write(line)
		o.close()
		i.close()

	# Load the config file. If it doesn't exist, create it
	def load_config(self):
		f = None
		path = os.path.join(winpaths.get_appdata(), "Dotannoy")

		# if the dotannoy folder in appdata doesn't exist, create it
		if not os.path.exists(path):
			os.makedirs(path)

		path = os.path.join(path, "config.json")
		log.info("Checking that {} exists".format(path))

		# if config.json exists, load it
		# if it doesn't, create a default config file
		if os.path.exists(path):
			log.info("Loading config.json")
			f = open(path, "r")
			self.config = json.load(f)
		else:
			log.info("Couldn't find config.json. Creating default config")
			f = open(path, "w")
			default_config = {"steamapps":""}
			json.dump(default_config, f, sort_keys=True, indent=4, separators=(',', ': '))
			self.config = default_config
			f.flush()
		f.close()

	# Save the config file to appdata
	def save_config(self):
		# save the config in appdata.
		f = open(os.path.join(winpaths.get_appdata(), "dotannoy\\config.json"), "w")
		json.dump(self.config, f, sort_keys=True, indent=4, separators=(',', ': '))
		f.flush()

		log.info("Saved {}".format(os.path.join(winpaths.get_appdata(), "dotannoy\\config.json")))
		f.close()

