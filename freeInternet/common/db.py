try:
    import sqlite3 as sqlite
except ImportError, e:
    import sqlite

class DBConnection(object):
    """
    Makes database connections easier
    """
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.db = sqlite.connect(self.path)
        self.cursor = self.db.cursor()
        return (self.db, self.cursor)

    def __exit__(self, type, value, traceback):
        self.db.commit()
        self.db.close()