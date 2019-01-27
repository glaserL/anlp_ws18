import requests
from bs4 import BeautifulSoup
from db import database as db
import time

def extract_data_from_HTML(html):
    page = BeautifulSoup(html, "html.parser")
    data = {}
    data['lyrics'] = page.find("div", class_ = "lyrics").get_text()
    try:
        year_raw = page.find("span", class_ = "metadata_unit-info metadata_unit-info--text_only").get_text()
    except AttributeError:
        # some sites don't have a date
        year_raw = "Unknown"
    data['year'] = year_raw.split(",")[-1].strip()
    return data


def main():
    database = db.Database()
    connection = database.get_connection()
    statements = []
    # prettify output
    cur = connection.cursor()
    cur.execute("SELECT id, genius_url FROM songs;")
    # connection.commit()
    try:
        from tqdm import tqdm
        iterator = tqdm(cur.fetchall())
    except ModuleNotFoundError:
        iterator = cur.fetchall()
    sql_statement = "UPDATE songs SET lyrics = :lyrics, year = :year WHERE id = :id;"
    for id, link in iterator:
        response = requests.get(link)
        # print(response)
        raw_html = response.text
        data = extract_data_from_HTML(raw_html)
        # sql_statement = "UPDATE songs SET "
        # sql_statement += (", ".join("%s = '%s'" % (key, value) for key, value in data.entries()))
        # sql_statement += "WHERE id = %s" % id
        # sql_statement += ";"
        data['id'] = id
        statements.append(data)
        if len(statements) > 500:
            connection = database.get_connection()
            connection.executemany(sql_statement, statements)
            connection.commit()
            statements.clear()
        time.sleep(0.2)
    # connection = database.get_connection()
    connection.executemany(sql_statement, statements) # clearup
    connection.commit()
    connection.close()


main()
# database = db.Database()
# connection = database.get_connection()

# cur = connection.cursor()
# cur.execute("SELECT id, genius_url FROM songs;")
# id, link = cur.fetchone()

xml = requests.get("https://genius.com/16koinzbry-16koinz-theme-song-lyrics")
xml
parse = BeautifulSoup(xml.text, "html.parser")
parse.find("div", class_ = "lyrics").get_text()
# result = ""
# parse.find("div", class_ = "lyrics").get_text()
# for x in parse.children:
#     print(x)

# parse.find("span", class_ = "metadata_unit-info metadata_unit-info--text_only").get_text()
