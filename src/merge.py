import argparse
from tqdm import tqdm
import sqlite3 as sqlite

def main(args):
    s_conn = sqlite.connect(args.source)
    t_conn = sqlite.connect(args.target)

    print("Loading from source..")
    s_select_statement = "SELECT artist, title, lyrics, year, genre, genius_url FROM songs WHERE lyrics IS NOT NULL;"
    s_cur = s_conn.cursor()
    s_cur.execute(s_select_statement)

    s_dict = {}
    for artist, title, lyrics, year, genre, url in s_cur.fetchall():
        if not args.silent and (artist, title) in s_dict.keys():
            print("WARNING CONFLICT %s, %s." % (artist,title))
        s_dict[(artist,title)] = (artist, title, lyrics,year, genre, url)
    
    print("DONE.")
    s_conn.close()
    del s_conn
    t_select_statement = "SELECT artist, title FROM songs"
    if args.dry:
        t_cur = t_conn.cursor()
        t_cur.execute(t_select_statement)
    
        for t_artist, t_title in t_cur.fetchall():
            if (t_artist, t_title) in s_dict.keys():
                s_artist, s_title, s_lyrics, s_year, s_genre, s_url = s_dict[(t_artist, t_title)]
                if s_artist == t_artist and s_title == t_title:
                    print("(Writing) %s - %s (%s): %s.." % (
                                s_artist, s_title, s_year, s_lyrics[:40] 
                    ))
                else:
                    print("WARNING MISSMATCH")
    else:
        sql_statements = []
        # t_update_statement = "UPDATE songs SET year = ?, lyrics = ? WHERE artist = ? AND title = ?;"
        t_insert_statement = ("INSERT INTO songs VALUES(NULL, :title, :artist, :year, :genre, :url, :lyrics, " 
    "NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);")
        t_cur = t_conn.cursor()
        # t_cur.execute(t_select_statement)
        # print("grabbed rows from target")
        try:
            from tqdm import tqdm
            iterator = tqdm(s_dict.keys())
            # for a,b in iterator:
            #     print(a,b)
            # print("Iterator %s." % type(iterator))
        except ModuleNotFoundError:
            iterator = s_dict.keys()
        # t_cur.close()
        # t_conn.commit()
        # t_conn.close()
        # print("Closed database")
        # del t_conn
        # print("Reopening")
        # t_conn = sqlite.connect(args.target)
        # t_cur = t_conn.cursor()
        print("Starting")
        c = 0
        for t_a,t_t in iterator:
            # print(".", end="")
            if (t_a, t_t) in s_dict.keys():
                s_artist, s_title, s_lyrics, s_year, s_genre, s_url = s_dict[(t_a, t_t)]
                write_data = {
                    "artist" : t_a,
                    "title" : t_t,
                    "lyrics" : s_lyrics,
                    "year" : s_year,
                    "genre" : s_genre,
                    "url" : s_url
                    }
                # print("Got shit from the in memory dict!")
                # sql_statements.append((s_year, s_lyrics, t_a, t_t))
                sql_statements.append(write_data)
                # print("Put shit in sql statements list!")
                # if len(sql_statements) > 2001:
                if c % 2000 == 0:
                    t_cur.executemany(t_insert_statement, sql_statements) 
                    sql_statements.clear()
                    t_conn.commit()
                c += 1
        t_cur.executemany(t_insert_statement, sql_statements) 
        sql_statements.clear()
        t_conn.commit()
        

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Params')
    parser.add_argument("-s", "--source", type = str,
                        required = True, help = "")
    parser.add_argument("-t", "--target", type = str,
                        required = True,help = "")
    parser.add_argument('--dry', action ="store_true",
                        help = "Won't write, just print.")
    parser.add_argument("--silent", action = 'store_true',
                        help = "Not too many prints")
    parser.add_argument("-n","--number_of_songs", type = int, default = 50,
                        help = "How many songs to get per artist")
    parser.add_argument('-g','--genre', nargs="*")
    args = parser.parse_args()
    main(args)
