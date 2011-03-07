import os
import commands
import unittest

import __init__

class TestSequenceFUnctions(unittest.TestCase):
    
    def setUp(self):
        self.directory = os.path.dirname(__init__.__file__)
        self.generator = __init__.input(self.directory, 3)
        
        self.seq = [
            (0, 7, 8, 19, 2),
            (8, 14, 8, 19, 2),
            (15, 22, 8, 19, 2)
        ]
    
    def test_input(self):
        self.assertEqual(
            self.seq,
            [i for i in self.generator]
        )
    
    def test_rm(self):
        binary_path = os.path.join(self.directory, "diffie_hellman")
        
        self.assertTrue(not os.path.exists(binary_path))
        
        commands.getoutput("touch %s" % binary_path)
        self.assertTrue(os.path.exists(binary_path))
        
        commands.getoutput("rm %s" % binary_path)
        self.assertTrue(not os.path.exists(binary_path))
    
if __name__ == '__main__':
    unittest.main()