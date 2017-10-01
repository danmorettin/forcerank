
"""This module contains a database manager that acts as an ORM."""

import sqlite3
from pandas import read_sql_query


class DatabaseManager():
    """Abstracts away the SQL statements.

    Attributes:
        conn: The connection to the database. conn is closed by __del__ if
              close() is forgotten.
        cur: The cursor for the database.
    """

    def __init__(self, ticker, filepath):
        self.ticker = ticker
        self.filepath = filepath
        self.df = None
        self.conn = sqlite3.connect(filepath,
                                    detect_types=sqlite3.PARSE_DECLTYPES |
                                    sqlite3.PARSE_COLNAMES)

    def __del__(self):
        if self.conn:
            self.conn.close()

    def read(self):
        self.df = read_sql_query("SELECT * FROM Prices;", self.conn)
        self.df.set_index('Dates', inplace=True)

    def close(self):
        if self.conn:
            self.conn.close()


def _test():
    ticker = 'GLD'
    db_path = ('/Users/Dan/Coding/Finance/projects/' +
               'forcerank/data/test_data/{}.db'.format(ticker))
    db = DatabaseManager(ticker, db_path)
    db.read()
    print(db.df)
    db.close()


if __name__ == "__main__":
    _test()
