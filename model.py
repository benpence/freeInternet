import commands

from itertools import chain, izip
import common

class Model(object):
    _CLASS_OBJECTS = {
        "_rows" : {},
        "_changes" : {},
        "_init" : False,
    }
    
    _SQLITE_CONVERSION = {
        "VARCHAR" : str,
        "INTEGER" : int,
    }
    
    def __init__(self, **columns):
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
        
        for column, kind in chain(self._keys.items(), self._values.items()):
            # Was passed into function
            if column in columns:
                self.__setattr__(column, columns[column])
                
            # Set to default value for type
            else:
                self.__setattr__(column, self._SQLITE_CONVERSION[kind]())


        # Insert row into memory
        self._rows[tuple((
            columns[column]
            for column in self._keys))] = self        

        # Creating new entry
        self._queueChange((columns[key] for key in self._keys), columns.keys(), currentNew=True) 
        

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
                "%s = %s" %
                    (str(key),
                    str(self.__getattribute__(key)))
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
        
        # No rows
        if not hasattr(cls, '_rows'):
            if _max == 1:
                return None
                
            return []
        
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
    def _queueChange(cls, key, columns, currentNew=False):
        """
        key:[str] | columns:[str] -> None
        
        Record change to write to database after _CHANGES_BEFORE_WRITE changes
        """
        
        if cls._reading:
            return
        
        key = tuple(key)
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
        if len(cls._changes) > common._CHANGES_BEFORE_WRITE:
            if not hasattr(cls, '_DATABASE_PATH'):
                cls.writeToDatabase(common._DATABASE_PATH)
            else:
                cls.writeToDatabase(cls._DATABASE_PATH)

    
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
        
        with common.db_connection(db_path) as (db, cursor):
            cursor.execute("SELECT * FROM %s" % cls.__name__)

            def unicodeToStr(value):
                if isinstance(value, unicode):
                    return str(value)
                else:
                    return value
                    
            column_names = cls._keys.keys() + cls._values.keys()
            for row in cursor.fetchall():
                cls(
                    **dict((
                        (column, unicodeToStr(row[i]))
                        for i, column in enumerate(column_names))))
        cls._reading = False

    @classmethod
    def writeToDatabase(cls, db_path):
        """
        db_path:str -> None
        
        Write memory to database (from cls._changes)
        """
        
        commands = []
        
        def addQuotes(element):
            if isinstance(element, str):
                return '"' + element + '"'
            else:
                return str(element)
    
        for key, (new, columns) in cls._changes.items():
            
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
        
        with common.db_connection(db_path) as (db, cursor):
            # Determine column datatypes
            sample = cls.search(1)
            
            table_attributes = ', '.join(
                ("%s %s" % (column_name, 
                            column_type)
                 for (column_name, column_type) in chain(cls._keys.items(), cls._values.items())))
                 
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

def test():
    commands.getoutput('rm database.db')
    
    class Person(Model):
        _DATABASE_PATH = 'database.db'
        _keys = {
            'first_name'    : 'VARCHAR',
            'last_name'     : 'VARCHAR',
            }
        _values = {
            'height'        : 'INTEGER',
            }
    
    class Building(Model):
        _DATABASE_PATH = 'database.db'
        _keys = {
            'name'          : 'VARCHAR',
            }
        _values = {
            'height'        : 'INTEGER',
            }
    
    for i in range(100):
        Person(first_name="Tom%d" % i,
               last_name="Sawyer%d" % i,
               height=i)
    tom = Person.search(1)
    tom.height = 99
        
if __name__ == "__main__":
    test()