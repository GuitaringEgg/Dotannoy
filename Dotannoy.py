import argparse
import Annoy
from Annoy import Annoy

parser = argparse.ArgumentParser(description="Generate a dota config that binds line from a text file to a key.")
parser.add_argument("--download", "-d",
                    help="download jokes from a site. Use -l for a list of sites available")
parser.add_argument("--list", "-l", action="store_true",
                    help="print a list of sites avaiable to download jokes from")
parser.add_argument("--default-puns", "-p", action="store_true",
					help="use the default list of puns stored in default.txt")
parser.add_argument("--input", "-i", metavar="file"
                    help="the file that the lines will be taken from")
parser.add_argument("--output", "-o", metavar="file"
                    help="the file that the config will be saved to")
parser.add_argument("--autoexec", "-a", action="store_false",
                    help="diable the appending of the execution of the script when Dota starts")
parser.add_argument("--force", "-f", action="store_true",
                    help="force jokes that exceed the line length to be trucated and saved anyway")

parser.add_argument("--say_key", "-sk", metavar="key",
					help="set the key that the say bind is set to")
parser.add_argument("--random_key", "-rk", metavar="key",
					help="set pthe key that randomises what to say next")

args = parser.parse_args()

annoy = Annoy(args)

