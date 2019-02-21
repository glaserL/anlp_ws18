import requests
from bs4 import BeautifulSoup
from db import database as db
import argparse
import time
import os
import random

def extract_data_from_HTML(html):
    page = BeautifulSoup(html, "html.parser")
    data = {}
    try:
        data['lyrics'] = page.find("div", class_ = "lyrics").get_text()
    except AttributeError:
        # some sites don't have lyrics
        data['lyrics'] = "N/A"
    try:
        year_raw = page.find("span", class_ = "metadata_unit-info metadata_unit-info--text_only").get_text().split(",")[-1].strip()
        if not year_raw.isdigit(): # quite a few year fields are filled weirdly
            year_raw = "N/A"
    except AttributeError:
        # some sites don't have a date
        year_raw = "N/A"
    data['year'] = year_raw
    return data


def main(args):
    database = db.Database()
    connection = database.get_connection()
    statements = []
    # prettify output
    cur = connection.cursor()
    # cur.execute("SELECT DISTINCT genre FROM songs;")
    # genres = [row[0] for row in cur.fetchall()]
    genres = args.genre
    for genre in genres:
        cur.execute("SELECT id, genius_url FROM songs WHERE lyrics IS NULL AND genre = '%s' ORDER BY id DESC;" % genre) # grab stuff that not filled
        responses = list(cur.fetchall())
        print("Got %s empty rows." % len(responses))
        block_length = len(responses)/args.machines
        start = int(block_length * args.id)
        end = int(block_length * (args.id + 1))
        print("Machine %s, scraping range %s to %s (%s total)." %
                (args.id, start, end, len(responses)))
        try:
            from tqdm import tqdm
            iterator = tqdm(responses[start:end])
        except ModuleNotFoundError:
            iterator = responses[start:end]
        sql_statement = "UPDATE songs SET lyrics = :lyrics, year = :year WHERE id = :id;"
        print("Crawling %s %s lyrics now.." % (len(iterator), genre))
        for id, link in iterator:
            response = requests.get(link)
            if not response.ok:
                print(response)
            raw_html = response.text
            data = extract_data_from_HTML(raw_html)
            
            data['id'] = id
            statements.append(data)
            if len(statements) > 200:
                connection = database.get_connection()
                connection.executemany(sql_statement, statements)
                connection.commit()
                statements.clear()
            time.sleep(0.1) # to not spam genius too much
            if len(statements) % 40 == 0:
                waittime = random.uniform(0.5,7) # have it seem like more a "human" interaction
                time.sleep(waittime)
        
    connection.executemany(sql_statement, statements) # clearup
    connection.commit()
    connection.close()

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Params')
    parser.add_argument('-g','--genre', nargs="*",
                        help = "How many songs to get per artist")
    parser.add_argument("-m","--machines", default = 1, type = int,
                        help = "How many different machines this will run on")
    parser.add_argument("-i","--id", default = 0, type = int,
                        help = "Which id this machine holds")
    args = parser.parse_args()
    main(args)
