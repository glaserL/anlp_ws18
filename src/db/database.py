import sqlite3
import sys
import os
class Database(object):
    # TODO: force db to end up in this directory.
    def __init__(self,
        path_to_db = os.path.dirname(os.path.abspath(__file__))+"/database.db",
        path_to_schema = os.path.dirname(os.path.abspath(__file__))+"/schema.sql"):
        self.conn = sqlite3.connect(path_to_db)

        c = self.conn.cursor()
        with open(path_to_schema, encoding='utf-8', mode='r') as f:
            query = f.read()
        c.execute(query)

    def get_connection(self):
        """Use this to get raw connection to operate with"""
        return self.conn

    def select(self, query, criteria, fetchone = False):
        """dumb recylable select statement sender, expects
        a query with named (!) values plus a dict."""
        cur = self.get_connection().cursor()
        cur.execute(query, criteria)
        if fetchone:
            return cur.fetchone()
        else:
            return cur.fetchall()

    def simple_query(self, columns = "*",
                        title = False,
                        artist = False,
                        genre = False,
                        # begin = False, TODO: implement
                        # end = False, TODO: implement
                        # generic_criteria = {}, TODO: implement
                        fetchone = False):
        """ general query, can then be customed by named arguments
        on what criteria
        """
        criteria = {}
        if title:
            criteria["title"] = title
        elif artist:
            criteria["artist"] = artist
        elif genre:
            criteria["genre"] = genre
        # elif begin:
        #     criteria["begin"] = begin
        # elif end:
        #     criteria["end"] = end
        statement = "SELECT "+",".join(columns)+" FROM songs WHERE "\
                    + ",".join([("%s=:%s" %
                            (key, key)) for key in criteria.keys()])\
                    + ";"
        print(statement)
        return self.select(statement, criteria, fetchone)





if __name__ == "__main__":
    # TODO: write bunch of tests
    pass
