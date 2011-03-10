import unittest

import fi.job

class TestSequenceFunctions(unittest.TestCase):

    def test_randomHash(self):
        _hash = fi.job.randomHash()
    
        self.assertEqual(
            len(_hash),
            fi.job.HASH_LENGTH
        )
    
        hashes = set()
        unique_num = 2000
    
        for i in range(unique_num):
            hashes.add(fi.job.randomHash())
        
        self.assertEqual(
            len(hashes),
            unique_num
        )


    def test_partition(self):
        self.assertEqual(
            fi.job.partition(range(1, 9), 3),
            [[1, 2, 3], [4, 5], [6, 7, 8]]
        )

        self.assertEqual(
            fi.job.partition(range(1, 11), 10),
            [[i] for i in range(1, 11)]
        )
        
if __name__ == '__main__':
    unittest.main()