from twisted.trial import unittest
import sqlite3

import fi
import fi.db

class TestSequenceFunctions(unittest.TestCase):
    
    def test_DBConnection(self):
        with fi.db.DBConnection('test.db') as (db, cursor):
            self.assertIsInstance(
                cursor,
                sqlite3.Cursor
            )