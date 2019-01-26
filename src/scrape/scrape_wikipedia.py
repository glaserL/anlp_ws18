from bs4 import BeautifulSoup
import requests
import csv
import re
SEEDFILE = "/Users/glaser/Developer/cogsys/github/anlp_ws18/src/scrape/seedfile.csv"
META_REGEX = re.compile("/wiki/([A-Z]).*:(.+)")


def scrape_artist_names_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    artist_links = []
    for link in soup.find_all('a'):
        href = str(link.get('href')) # returns as NoneType, cast to string, TODO: typecheck?
        if href.startswith("/wiki") and not META_REGEX.match(href): # TODO: Remove (rapper) and shit like that
            artist_links.append(href.replace("_", " ").replace("/wiki/",""))
    return artist_links

with open(SEEDFILE, 'r', encoding = 'utf-8') as f:
    print("genre;artist;url")
    for line in f:
        genre, url = line.strip().split(";")
        r = requests.get(url)
        for artist in scrape_artist_names_from_html(r.content):
            print("%s;%s;%s" % (genre, artist, url))
