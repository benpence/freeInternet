import unittest

import fi

class TestSequenceFunctions(unittest.TestCase):
            
    def test_isNumber(self):
        self.assertTrue(
            reduce(
                lambda x, y: x and y,
                map(
                    lambda x: fi.isNumber(x),
                    ('33', '-1', '0', '1', '1.0', '1.55e20')
                )
            )
        )
        
        self.assertTrue(
            not reduce(
                lambda x, y: x or y,
                map(
                    lambda x: fi.isNumber(x),
                    ('aa', [1], {1:5}, (5, 1))
                )
            )
        )

    
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
        
    def test_execute(sefl):
        self.assertEqual(
            fi.execute("echo 'eee'")
            'eee'
        )
        
if __name__ == '__main__':
    unittest.main()