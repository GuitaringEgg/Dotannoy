import random

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
