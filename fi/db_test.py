import unittest

import fi
import fi.db

class TestSequenceFunctions(unittest.TestCase):
    
    def test_DBConnection():
        
        with db.DBConnection() as (db, cursor):
            cursor.execute("SELECT * FROM %s" % cls.__name__)
    
    
    
if __name__ == '__main__':
    unittest.main()