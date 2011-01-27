from itertools import chain, izip
from twisted.internet import defer

try:
    import sqlite3 as sqlite
except ImportError, e:
    import sqlite
    print "'import sqlite3' failed. Using sqlite"



class Model(object):
    _CHANGES_BEFORE_WRITE = 10
    _DATABASE_PATH = 'database.db'
    
    _CLASS_OBJECTS = {
        "_rows" : {},
        "_changes" : {},
        "_init" : False,
    }
    
    def __init__(self, columns):
        object.__init__(self)
        
        # These setters are basically a class __init__
        if not hasattr(self.__class__, '_rows'):
            self.__class__._rows = {}
        if not hasattr(self.__class__, '_changes'):
            self.__class__._changes = {}
        if not hasattr(self.__class__, '_init'):
            self.__class__._init = False
        if not hasattr(self.__class__, '_reading'):
            self.__class__._reading = False
        
        # Improper row insertion?
        if not self._keys <= columns.keys():
            """ERROR"""
            return
        
        # Turn auto-queueing changes off
        self._init = True
        
        for column, value in columns.items():
            self.__setattr__(column, value)
        
        # Creating new entry
        self._queueChange(self._keys, columns.keys())
        
        # Insert row into memory
        self._rows[tuple((
            columns[column]
            for column in self._keys))] = self
        
        # Turn auto-queuing changes on
        self._init = False
                
    def __str__(self):
        """
        None -> self_string:str
        
        Returns in format Class : (value1, value2,...)
        """
        return "%s : (%s)" % (
            self.__class__.__name__,
            ', '.join((
                str(self.__getattribute__(key))
                for key in chain(self._keys, self._values))))
    
    @classmethod
    def search(cls, _max=None, **kwargs):
        """
        _max:int | columns:{column:value} -> [cls]
        
        Query table in this fashion:
            TableName.search(5, # max rows
                             column_name1=value1,
                             column_name1=value2
                             )
        """
        
        # Return whole table
        if not kwargs and not _max:
            return cls._rows.values()
        
        # Lookup by hash if keys specified
        if set(cls._keys) <= set(kwargs.keys()):
            return cls._rows.get(tuple(kwargs[key]
                                        for key in cls._keys),
                                 ())

        # Lookup by comparing fields
        results = []
        for (key, row) in cls._rows.items():
            invalid = False
            for column in kwargs:
                if row.__getattribute__(column) != kwargs[column]:
                    invalid = True

            if not invalid:
                results.append(row)

        # Return value instead of list if desired
        if _max == 1 and results:
            return results[0]
            
        return results[:_max]
    
    @classmethod
    def _queueChange(cls, key, columns):
        """
        key:[str] | columns:[str] -> None
        
        Record change to write to database after _CHANGES_BEFORE_WRITE changes
        """
        
        if cls._reading:
            return
        
        key = tuple(key)
        currentNew = key not in cls._rows
        currentColumns = set(columns)
                    
        # Update change entry
        if key in cls._changes:
            oldNew, oldColumns = cls._changes[key]
            
            # Keep new entries as new entries and a SET of all modified columns
            cls._changes[key] = (currentNew | oldNew, oldColumns | currentColumns)
            
        # New entry in _changes for this table and keys
        else:
            cls._changes[key] = (currentNew, currentColumns)
            
        # Write to disk?
        if len(cls._changes) == cls._CHANGES_BEFORE_WRITE:
            cls._writeToDatabase()

    
    def __setattr__(self, attr, value):
        """
        attr:str | value:? -> None
        
        Add hook to automatically record changes to the database
        """
        superSetter = super(Model, self).__setattr__

        # Bypass during __init__() to avoid complicated recursion mess
        if not self._init:
            if attr in self._values:
                superSetter(attr, value)
                keys = (self.__getattribute__(key)
                        for key in self._keys)
                        
                self._queueChange(keys,
                                  [attr])
                                  
            superSetter(attr, value)
            
        # Otherwise, carry on as normal
        else:
            superSetter(attr, value)

    @classmethod
    def readIntoMemory(cls, db_path):
        """
        db_path:str -> None
        
        Read database into memory
        """
        cls._reading = True

        cls._rows = {}
        cls._changes = {}
        
        with db_connection(cls._DATABASE_PATH) as (db, cursor):
            cursor.execute("SELECT * FROM %s" % cls.__name__)

            def unicodeToStr(value):
                if isinstance(value, unicode):
                    return str(value)
                else:
                    return value
                    
            column_names = cls._keys + cls._values
            for row in cursor.fetchall():
                cls(
                    dict((
                        (column, unicodeToStr(row[i]))
                        for i, column in enumerate(column_names))))
        cls._reading = False

    @classmethod
    def _writeToDatabase(cls, db_path):
        """
        db_path:str -> None
        
        Write memory to database (from cls._changes)
        """
        
        commands = []
    
        for key, (new, columns) in cls._changes.items():
            def addQuotes(element):
                if isinstance(element, str):
                    return '"' + element + '"'
                else:
                    return str(element)
            
            # Create appropriate query        
            if new:
                command = "INSERT INTO %s" % cls.__name__
            
                # Column names to be updated
                command += '(%s) ' % ', '.join(columns)
                      
                # Values to be updated
                values = []
                
                command += 'VALUES (%s) ' % ', '.join((
                    f(cls._rows[key].__getattribute__(column))
                    for column in columns
                    for f in [addQuotes]))
            
            else:
                command = "UPDATE %s" % cls.__name__
            
                # Set column = new_value for each modified column
                command += " SET"
                command += ', '.join((" %s = %s" % (
                    column, f(cls._rows[key].__getattribute__(column)))
                    for column in columns
                    for f in [addQuotes]))

                # Get row from keys
                command += " WHERE"
                
                command += 'AND'.join((
                    " %s = %s " % (
                        key_name, f(cls._rows[key].__getattribute__(key_name)))
                        for key_name in cls._keys
                        for f in [addQuotes]))
            commands.append(command)
        
        with db_connection(cls._DATABASE_PATH) as (db, cursor):
            # Create tables if they don't exist
            pythonToSQL = {
                int : "INTEGER",
                str : "VARCHAR",
            }
        
            # Determine column datatypes
            sample = cls.search(1)
            
            table_attributes = ', '.join(
                ("%s %s" % (column_name, 
                            pythonToSQL.get(sample.__getattribute__(column_name).__class__,
                                            "VARCHAR"))
                 for column_name in chain(cls._keys + cls._values)))
                 
            # Create table if first write
            create_table = "CREATE TABLE IF NOT EXISTS %s(%s, PRIMARY KEY(%s))" % (
                 cls.__name__,
                 table_attributes,
                 ', '.join(cls._keys))
            cursor.execute(create_table)
                    
            # Execute commands to mirror database to in-memory changes
            for command in commands:
                cursor.execute(command)
                    
        cls._changes = {}

class db_connection(object):
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


def test():
    class Person(Model):
        _keys = [
            'first_name',
            'last_name'
            ]
        _values = [
            'height']
    
    class Building(Model):
        _keys = [
            'name'
            ]
        _values = [
            'height'
            ]
    
    Person.readIntoMemory('database.db')
    tom = Person.search(1)
    tom.height = 99
    Person._writeToDatabase('database.db')
    Person.readIntoMemory('database.db')
    Person._writeToDatabase('database.db')
        
if __name__ == "__main__":
    test()