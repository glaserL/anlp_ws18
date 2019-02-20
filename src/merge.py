import sqlite3 as sqlite
import argparse

def main(args):
    source_conn = sqlite.connect(args.source_path)
    target_conn = sqlite.connect(args.source_path)

    # first, we grab all written lyrics from the source database
    # and store them in memory for easy access and sanity checks.
    source_cur = source_conn.cursor()
    source_select_query = "SELECT artist, title, lyrics, year FROM songs WHERE lyrics IS NOT NULL;"
    source_cur.execute(source_select_query)
    source_dict = {}
    for artist, title, lyrics, year in source_cur.fetchall():
        if (artist, title) in source_dict.keys():
            if args.dry:
                print("WARNING! DOUBLE ID WHEN READING (%s, %s)" % (artist, title))
        source_dict[(artist, title)] = (artist, title, lyrics, year)
    print("Loaded %s entries from source database." % (
                    len(source_dict)))
    # then, write them to the database, also checking for missings,
    # doubles or inconsistent data.
    target_cur = target_conn.cursor()
    if args.dry:
        target_select_query = "SELECT artist, title, lyrics FROM songs;"
        target_cur.execute(target_select_query)
        for target_artist, target_title, target_lyrics in target_cur.fetchall():
            if (target_artist, target_title) in source_dict.keys():
                source_artist, source_title, source_lyrics, source_year = source_dict[(target_artist, target_title)]
                del source_dict[(target_artist, target_title)]
                if source_artist == target_artist and source_title == target_title and not args.silent:
                    print("(Writing) %s by %s (%s): %s.." % (target_title,
                                                            target_artist,
                                                            source_year,
                                                            source_lyrics[:40]))
                if source_artist != target_artist:
                    print("MISMATCH artist! source: %s, target: %s." % (source_artist, target_artist))
                if source_title != target_title:
                    print("MISMATCH title! source: %s, target: %s." % (source_title, target_title))
        if len(source_dict):
            print("LEFTOVER DATA, %s SOURCE ENTRIES. Possibly you wrote that already?" % len(source_dict))
    else:
        target_cur.close()
        source_conn.close()
        source_conn = sqlite.connect(args.source_path)
        target_cur = source_conn.cursor()
        sql_update_statement = "UPDATE songs SET lyrics = ?, year = ? WHERE artist = ? AND title = ?;"
        statements = []
        target_select_query = "SELECT artist, title FROM songs;"
        target_cur.execute(target_select_query)
        
        try:
            from tqdm import tqdm
            iterator = tqdm(list(target_cur.fetchall()))
        except ModuleNotFoundError:
            iterator = list(target_cur.fetchall())
        for artist, title in iterator:
            if (artist, title) in source_dict.keys():
                artist, title, lyrics, year = source_dict[(artist, title)]
                statements.append((lyrics, year, artist, title))
                if len(statements) > 5000:
                    print("Writing right now")
                    target_conn.executemany(sql_update_statement, statements)
                    target_conn.commit()
                    statements.clear()
                    print("%s\r" % (10*" "))
                if len(statements) % 500 == 0:
                    print(".",end="")
        target_conn.executemany(sql_update_statement, statements)
        target_conn.commit()
        target_conn.close()
    print("weird endless loop")

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Params')
    parser.add_argument('-s','--source_path', required = True,
                        help = 'Where to pull from')
    parser.add_argument('-t', '--target_path', required = True,
                        help = 'where to write to')
    parser.add_argument('--dry', action = 'store_true',
                        help = 'Just print, dont write.')
    parser.add_argument("--silent", action = 'store_true',
                        help = 'Only prints errors.')
    args = parser.parse_args()
    main(args)
