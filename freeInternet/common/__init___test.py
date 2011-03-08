import unittest

import __init__

class TestSequenceFunctions(unittest.TestCase):

    def test_randomHash(self):
        _hash = __init__.randomHash()
        
        self.assertEqual(
            len(_hash),
            32
        )
        
        hashes = set()
        unique_num = 2000
        
        for i in range(unique_num):
            hashes.add(__init__.randomHash())
            
        self.assertEqual(
            len(hashes),
            unique_num
        )

    def test_isNumber(self):
        self.assertTrue(
            reduce(
                lambda x, y: x and y,
                map(
                    lambda x: __init__.isNumber(x),
                    ('33', '-1', '0', '1', '1.0', '1.55e20')
                )
            )
        )
        
        self.assertTrue(
            not reduce(
                lambda x, y: x or y,
                map(
                    lambda x: __init__.isNumber(x),
                    ('aa', [1], {1:5}, (5, 1))
                )
            )
        )

    def test_partition(self):
        self.assertEqual(
            __init__.partition(range(1, 9), 3),
            [[1, 2, 3], [4, 5], [6, 7, 8]]
        )
        
        self.assertEqual(
            __init__.partition(range(1, 11), 10),
            [[i] for i in range(1, 11)]
        )
        
if __name__ == '__main__':
    unittest.main()