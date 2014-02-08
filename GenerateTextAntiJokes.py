import urllib2
from bs4 import BeautifulSoup

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
