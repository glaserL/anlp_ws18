import requests
from bs4 import BeautifulSoup
from db import database as db
import time
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


def main():
    database = db.Database()
    connection = database.get_connection()
    statements = []
    # prettify output
    cur = connection.cursor()
    cur.execute("SELECT DISTINCT genre FROM songs;")
    genres = [row[0] for row in cur.fetchall()]
    for genre in genres:
        cur.execute("SELECT id, genius_url FROM songs WHERE lyrics IS NULL AND genre = '%s';" % genre) # grab stuff that not filled
        try:
            from tqdm import tqdm
            iterator = tqdm(cur.fetchall())
        except ModuleNotFoundError:
            iterator = cur.fetchall()
        sql_statement = "UPDATE songs SET lyrics = :lyrics, year = :year WHERE id = :id;"
        print("Crawling %s lyrics now.." % genre)
        for id, link in iterator:
            response = requests.get(link)
            if not response.ok:
                print(response)
            raw_html = response.text
            data = extract_data_from_HTML(raw_html)
            
            data['id'] = id
            statements.append(data)
            if len(statements) > 2000:
                connection = database.get_connection()
                connection.executemany(sql_statement, statements)
                connection.commit()
                statements.clear()
            time.sleep(0.1) # to not spam genius too much
            if len(statements) % 25 == 0:
                waittime = random.uniform(0.5,10) # have it seem like more a "human" interaction
                time.sleep(waittime)
        
    connection.executemany(sql_statement, statements) # clearup
    connection.commit()
    connection.close()


main()
