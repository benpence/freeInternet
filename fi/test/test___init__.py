from twisted.trial import unittest

import fi

class TestSequenceFunctions(unittest.TestCase):
    
    def test_invalidArgs(self):
        rules = (
            ('Ben', 'John', 'Peter'),
            {'Pence': 55, 'Beal': 100, 'Woods': 1000},
            ['Swimmer', 'Commander', 'Artist']
        )
        usage = "Usage: %s {Ben|John|Peter} {Pence|Beal|Woods} {Swimmer|Commander|Artist}"
        
        self.assertTrue(
            not fi.invalidArgs(
                ('test test', 'Ben', 'Pence', 'Swimmer'),
                rules
            )
        )
            
        self.assertEqual(
            fi.invalidArgs(
                ('hey look at me', 'JJJ', 'Pence', 'Swimmer'),
                rules
            )(),
            usage % 'hey look at me'
        )
        
        self.assertEqual(
            fi.invalidArgs(
                ['my test program'],
                rules
            )(),
            usage % 'my test program'
        )
        
    def test_execute(self):
        self.assertEqual(
            fi.execute("echo 'eee'").strip(),
            'eee'
        )