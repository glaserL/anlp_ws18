import requests
from pprint import pprint
import time
from tqdm import tqdm
import csv
# from db import database as db # imports a linked directory lol python suxx ass
import json

## Setup Genius session
# ACCESS_TOKEN = open("../config.json") # TODO: read access token from file 
SESSION = requests.Session()
SESSION.headers = {'application': 'ANLP Project',
       'User-Agent': 'http://github.com/glaserL/anlp_ws18'}
SLEEP_MIN = 0.2  # Enforce minimum wait time between API calls (seconds)
# SESSION.headers['authorization'] = 'Bearer ' + ACCESS_TOKEN
MAX_BATCH_SIZE = 1000

def find_artist_id(artist_name, max_request = 1):
    search_url = 'https://api.genius.com/search/'
    params = {'q' : artist_name, 'per_page' : 20}
    for i in range(max_request): # multiple Request still aint working
        params['page'] = i
        response = SESSION.request("GET", search_url ,params = params)
        results = response.json()['response']['hits']
        for result in results:
            primary_artist = result['result']['primary_artist']
            if primary_artist['name'] == artist_name:
                return primary_artist['id']
        time.sleep(0.2)
    return ""


def get_songs_for_artist(id, max_request = 1):
    search_url = 'https://api.genius.com/artists/%s/songs'
    params = {'q' : id, 'per_page' : 50}
    result = []
    for i in range(1, max_request+1): # 0 indices causes invalid page error
        params['page'] = i
        response = SESSION.request("GET", search_url % id, params = params)
        songs = response.json()['response']['songs']
        for song in songs:
            if song['lyrics_state'] == 'complete': # filter out garbage
                result.append({
                    'title' : song['title'],
                    'artist' : song['primary_artist']['name'],
                    'url' : song['url']
                })
        time.sleep(0.2)
    return result

# def collect_raw_songdata(artist_ids):
#     database = db.Database()
#     connection = database.get_connection()
#     statements = []
#     # prettify output 
#     try:
#         from tqdm import tqdm
#         iterator = tqdm(artist_ids)
#     except ModuleNotFoundError:
#         iterator = artist_ids
#     sql_statement = "INSERT INTO songs VALUES(NULL, :title, :artist, NULL, NULL, :url, NULL);"
#     for artist_id in iterator:
#         songs_of_artist = get_songs_for_artist(artist_id)
#         statements.extend(songs_of_artist)
#         if len(statements) > 1:
#             connection.executemany(sql_statement, statements) 
#             connection.commit()
#             statements.clear()
#     connection.executemany(sql_statement, statements) # clearup
#     connection.commit()
#     connection.close()

# collect_raw_songdata([430404])

# id = 430404
# get_songs_for_artist(id,3)
# search_url = 'https://api.genius.com/artists/%s/songs'
# params = {'q' : id, 'per_page' : 50, 'encoding' : 'utf-8'}
# result = []
# response = SESSION.request("GET", search_url % id, params = params)
# response.json()['response']['songs'][0].keys()

# response.json()['response']['songs'][2]['title']
# response.json()['response']['songs'][2]['primary_artist']['name']
# for i in range(1, max_request+1): # 0 indices causes invalid page error
#     params['page'] = i
#     response = SESSION.request("GET", search_url % id, params = params)

# response.json()['response']['songs'][0]['url']
# with open("/Users/glaser/Developer/cogsys/github/anlp_ws18/src/scrape/hipHopArtists.csv", 'r', encoding = 'utf-8') as f:
#     file = csv.DictReader(f, delimiter = ';')
#     for entry in tqdm(list(file)):
#         artist_name = entry['artist']
#         print(artist_name,";",find_artist_id(artist_name))
