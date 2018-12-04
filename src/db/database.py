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

    def get_songs(self, title = "", others = []):
        """ general query, can then be customed by named arguments
        on what criteria
        """
        raise MethodNotImplementedError

if __name__ == "__main__":
    # TODO: write bunch of tests
    pass
