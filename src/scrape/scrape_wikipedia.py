from bs4 import BeautifulSoup
import requests
import csv
import re
from db import database
import argparse

META_REGEX = re.compile("/wiki/([A-Z]).*:(.+)")

def scrape_artist_names_from_html(html):
    """ Runs through a wikipedia pages collecting names of artists
    """
    soup = BeautifulSoup(html, 'html.parser')
    artist_links = []
    for link in soup.find_all('a'):
        href = str(link.get('href')) # returns as NoneType, cast to string,
        if href.startswith("/wiki") and not META_REGEX.match(href):
            artist_links.append(href.replace("_", " ").replace("/wiki/",""))
    return artist_links

def main(args):

    with open(args.seedfile, 'r', encoding = 'utf-8') as f:
        # Setup
        sql_statement = "INSERT INTO scrape VALUES (NULL, ?, ?, NULL, NULL, ?);"
        statements = []
        db = database.Database()
        conn = db.get_connection()
        print("Scraping artist from %s" % args.seedfile)
        for line in f:
            # read seedfile with wikipedia urls
            genre, url = line.strip().split(";")
            r = requests.get(url)
            for artist in scrape_artist_names_from_html(r.content):
                # write batchwise 
                statements.append((artist,url, genre))
                if len(statements) > 1000:
                    conn.executemany(sql_statement, statements)
                    conn.commit()
                    statements.clear()
                    print(".", end = "")
        conn.executemany(sql_statement, statements)
        conn.commit()
        conn.close()
        print()

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Params')
    parser.add_argument('-s','--seedfile', type = str, required = True,
                        help = "csv seedfile to scrape from.")
    args = parser.parse_args()
    main(args)
