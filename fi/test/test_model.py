from twisted.trial import unittest

import fi
from fi import model
from fi import exception

class TestSequenceFunctions(unittest.TestCase):    

    def setUp(self):
        class ModelTest(model.Model):
            _keys = {
                'first'  : 'INTEGER',
                'second' : 'VARCHAR',
                }
            _values = {
                'third'  : 'INTEGER',
                'fourth' : 'VARCHAR',
            }
        
            def getRows(cls):
                return cls._rows
        
            def getFirst(self):
                return self.first
                
        self.model = ModelTest
                
    def test_creation(self):
        for variable in ('_rows', '_changes', '_init', '_reading'):
            self.assertTrue(
                not hasattr(
                    self.model,
                    variable
                )
            )

        """TODO: Figure out why __init__'s exception is not being caught"""
        """self.assertRaises(
            exception.InitializeError,
            self.model
        )
        
        self.assertRaises(
            exception.InitializeError,
            self.model,
            first=55
        )"""
        
        instance = self.model(
            first=55,
            second='hello world'
        )
        
        self.assertEqual(
            instance.getRows(),
            {('hello world', 55): instance}
        )
        
        self.assertEqual(
            instance._changes,
            {('hello world', 55): (True, set(['second', 'first']))}
        )
    
    def test_search(self):
        instance = self.model(
            first=55,
            second='hello world'
        )
        
        self.assertEqual(
            self.model.search(),
            [instance]
        )
        
        sibling = self.model(
            first=66,
            second='hello world'
        )
        
        self.assertEqual(
            self.model.search(),
            [instance, sibling]
        )
        
        self.assertEqual(
            self.model.search(first=55),
            [instance]
        )
        
        self.assertEqual(
            self.model.search(1, second='hello world'),
            instance
        )
        
        self.assertEqual(
            self.model.search(10, first=22),
            []
        )
            
    def test_database(self):
        fi.execute('touch test.db')
        
        self.model(
            first=55,
            second='hello world'
        )
        
        self.model(
            first=56,
            second='hey there'
        )
        
        self.model.writeToDatabase('test.db')
        self.model._rows = self.model._changes = None
        self.model.readIntoMemory('test.db')
        
        first, second = self.model.search()
        
        self.assertEqual(
            (first.first, first.second, second.first, second.second),
            (56, 'hey there', 55, 'hello world')
        )
    
    def tearDown(self):
        fi.execute('rm test.db &> /dev/null')