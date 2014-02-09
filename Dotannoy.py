import argparse
import Annoy

parser = argparse.ArgumentParser(description="Generate a dota config that binds line from a text file to a key.")
parser.add_argument("--sickipedia-top-100", "-stop", action="store_true", 
					help="download the top 100 jokes this week on sickipedia")
parser.add_argument("--sickipedia-random", "-sran",action="store_true",
					help="download random jokes from sickipedia")
parser.add_argument("--anti-jokes-random", "-ajran",action="store_true",
					help="download random anti jokes from anti-jokes.com")
parser.add_argument("--anti-jokes-top", "-ajtop", action="store_true",
					help="download the top jokes from anti-jokes.com")
parser.add_argument("--default-puns", "-d", action="store_true",
					help="use the default list of puns stored in default.txt")

parser.add_argument("--say_key", "sk", 
					help="the key that the say bind is set to")
parser.add_argument("--random_key", "-rk", 
					help="the key that randomises what to say next")

args = parser.parse_args()
