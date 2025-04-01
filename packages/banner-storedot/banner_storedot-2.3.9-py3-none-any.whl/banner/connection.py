
from typing import Union, Dict, Iterable
from abc import ABC, abstractmethod
from enum import Enum
from itertools import chain
from json import loads, dumps
from inspect import getfullargspec
from copy import deepcopy

from MySQLdb import connect as mysql_connect, MySQLError
from MySQLdb._exceptions import OperationalError
from MySQLdb.cursors import DictCursor

from psycopg2 import connect as postgres_sql_connect, Error as PostgresSQLError
from psycopg2.extras import RealDictCursor
from psycopg2.errors import DatabaseError as PostgresSQLDatabaseError
import redis
from redis.commands.json.path import Path
from pandas import DataFrame, Series, concat

try:
    from pandas.core.computation.ops import UndefinedVariableError # pandas < 1.5.0
    
except ImportError:
    from pandas.errors import UndefinedVariableError 

from numpy import int64

from banner.utils.const import TTL_KWARG, NW_CACHE_COLUMNS
from banner.utils.misc import digested_key #Banner
from banner.utils.pandas import parse_mysql_to_pandas_query
from banner.utils.web2py import LABEL_TO_COLUMN
from banner.utils.neware import calculate_dqdv

class ConnectionType(Enum):
    ''' What connection types are supported by ConnectionFactory'''
    mysql = 'mysql'
    redis = 'redis'
    postgres = 'postgres'

class ConnectionFactory(object):
    ''' Create and return a Connection based on given data, defaults to MySqlConnection'''
    def __new__(self, con_type: Union[ConnectionType, str] = ConnectionType.mysql, **kwargs):
        try:
            con_type = ConnectionType[con_type]

        except KeyError:
            pass
            
        if not isinstance(con_type, ConnectionType):
            raise TypeError('Unknown Connection Type')
        
        if con_type is ConnectionType.redis:
            return RedisConnection(**kwargs)
            
        return MySqlConnection(**kwargs)        

class Connection(ABC):
    ''' Abstract Connection, Defines Connection required methods '''
    @abstractmethod
    def retrieve(self):
        pass

    @abstractmethod
    def store(self):
        pass

class RelationalConnection(Connection):
    ''' A Relcational Connection'''
    @abstractmethod
    def describe(self, table: str = ''):
        pass

class Storage(Connection):
    ''' A Key/Value Connection'''
    @abstractmethod
    def keys(self, query):
        pass

class PrintableConnection(Connection):
    ''' print mixin'''
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass

class RedisConnection(Storage, PrintableConnection):
    ''' Connection with Redis db which is a printable Storage(Connection) '''
    HOUR = 3600

    def __init__(self, host, port=6379, passwd=None, db=0, ssl_key=None, ssl_cert=None, ssl_ca_cert=None, name=None, ttl=HOUR):
        self.data = dict(
            host=host,
            port=port,
            password=passwd,
            db=db,
            ssl_keyfile=ssl_key,
            ssl_certfile=ssl_cert,
            ssl_ca_certs=ssl_ca_cert,
            ssl=any([ssl_key, ssl_cert, ssl_ca_cert])
        ) # all args and kwargs are stored in here

        self.__ttl = ttl or RedisConnection.HOUR # default ttl used
        self.__name = name # connection name

        # Redis manages opening/closing by itself, it is safe to init it here
        self.instance = redis.Redis(
            **self.data, 
            decode_responses=True
        ) # The actual instance of redis
    
    def keys(self, query: str):
        '''
            Retrieve Keys from Storage
        '''
        return self.instance.keys(pattern=f'{str(query)}')

    def retrieve(self, func: callable, *args, **kwargs):
        '''
            Retrieve Value from Storage for a callable
        '''
        controller = QUERY_TO_STORAGE_CONTROL.get(
            func.__name__, DefaultStorageController
        ) # Try get storage controller based on func, otherwise DefaultStorageController

        return controller.retrieve(
            self.instance, func, *args, **kwargs
        ) # Use the controller to get value from db
        
    def store(self, value, func: callable, *args, ttl=None, nx=True, **kwargs):
        '''
            Set Value Into Storage
        '''
        ttl = ttl if ttl else self.__ttl # determine ttl

        controller = QUERY_TO_STORAGE_CONTROL.get(
            func.__name__, DefaultStorageController
        ) # Try get storage controller based on func, otherwise DefaultStorageController
        
        return controller.store(
            self.instance, value, func, *args, ttl=ttl, nx=nx, **kwargs
        ) # Use the controller to store value in db

    def retrieve_by(self, keys: Union[str, list]): #TODO support json
        ''' retrieve an str or a list of strs '''
        if isinstance(keys, str):
            return self.instance.get(keys)
        
        return self.instance.mget(keys)
        
    def store_by(self, key: str, value, ttl=None, nx=True):
        ''' 
            store value under key, for ttl 
            force update if nx=False
        '''
        ttl = ttl if ttl else self.__ttl

        resp = self.instance.set(
            key, value, ex=ttl, nx=nx
        )

        if resp is True:
            return key

        raise KeyError(f'{key} Exists')
        
    @property
    def name(self): # name of the connection
        return self.__name or str(self.data)

    def __str__(self): 
        return self.name
            
class MySqlConnection(RelationalConnection, PrintableConnection):
    ''' Connection with Mysql db which is a printable RelationalConnection(Connection) '''
    def __init__(self, host, user, port=3306, passwd=None, db=None, ssl_key=None, ssl_cert=None, charset='utf8', use_unicode=True, name=None):
        self.data = dict(
            host=host,
            user=user,
            port=port,
            passwd=passwd,
            db=db,
            ssl=dict(key=ssl_key, cert=ssl_cert),
            charset=charset,
            use_unicode=use_unicode,
            cursorclass=DictCursor 
        )  # all args and kwargs are stored in here

        self.__name = name

    def retrieve(self, query: str):
        ''' 
            get value(df) for mysql query(str) 
        '''
        try:
            instance = self.__connect()
            
            cursor = instance.cursor()
            
            cursor.execute(query) # the actualy query

            records = cursor.fetchall()

            cursor.close()
        
            records = DataFrame(records).convert_dtypes()
            
        except MySQLError as e:
            raise e
        
        finally:
            self.__close(instance) # handle closing the connection       

        return records

    def store(self, statement: str, *args, unique_checks=True, foreign_key_checks=True):
        ''' execute mysql statement for updating db data '''
        prefix, suffix = list(), list()

        if not unique_checks:
            prefix.append('SET unique_checks=0;')
            suffix.insert(0, 'SET unique_checks=1;')

        if not foreign_key_checks:
            prefix.append('SET foreign_key_checks=0;')
            suffix.insert(0, 'SET foreign_key_checks=1;')

        try:
            instance = self.__connect()
            
            cursor = instance.cursor()
            
            for q in prefix:
                cursor.execute(q)

            cursor.execute(statement, *args) # the actualy query
            
            for q in suffix:
                cursor.execute(q)
            
            instance.commit()
            
            cursor.close()
            
        except MySQLError as e:
            instance.rollback() # if an error occures, rollback
            raise e
        
        finally:
            self.__close(instance) # handle closing the connection
        
        return cursor.rowcount # return number of updated rows

    def describe(self, table: str = ''):
        ''' Describe table or whole schema '''
        _query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.data.get('db')}'"

        if table:
            _query = f'DESCRIBE {table}'

        return self.retrieve(_query)

    def __connect(self):
        try:
            return mysql_connect(**self.data)

        except OperationalError:
            raise MySQLError(
                f'Connection to {self.name} Failed'
            )
      
    def __close(self, instance):
        try:
            instance.close() 
            
        except (AttributeError, MySQLError):
            pass
    
    @property
    def name(self):
        return self.__name or str(self.data)

    def __str__(self):
        return self.name

class PostgresSqlConnection(RelationalConnection, PrintableConnection):
    ''' Connection with Postgressql db which is a printable RelationalConnection(Connection) '''
    def __init__(self, host, user, port=5432, passwd=None, db=None, ssl_key=None, ssl_cert=None, charset='utf8', name=None):
        self.data = dict(
            host=host,
            port=port,
            user=user,
            password=passwd,
            dbname=db,
            sslkey=ssl_key,
            sslcert=ssl_cert
        )

        self.__name = name
        self.__charset = charset
        
    def retrieve(self, query: str):
        ''' 
            get value(df) for mysql query(str) 
        '''
        try:
            instance = self.__connect()
            
            cursor = instance.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(query)  # the actualy query
            
            records = cursor.fetchall()
            
            cursor.close()
        
            records = DataFrame(records).convert_dtypes()

        except PostgresSQLError as e:
            raise e
        
        finally:
            self.__close(instance) # handle closing the connection     

        return records

    def store(self, statement: str):
        try:
            instance = self.__connect()
            
            cursor = instance.cursor()
            
            cursor.execute(statement)

            instance.commit()
            
            cursor.close()
            
        except PostgresSQLDatabaseError as e:
            instance.rollback() # if an error occures, rollback
            raise e
        
        finally:
            self.__close(instance) # handle closing the connection

        return cursor.rowcount

    def describe(self, table: str = ''):
        ''' Describe table or whole schema '''
        _query = f"SELECT table_name FROM information_schema.tables"

        if table:
            _query = (
                'SELECT column_name as "Field", data_type as "Type", is_nullable as "Null", column_default as "Default"'
                f" FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}'"
            )
            
        return self.retrieve(_query)
    
    def __connect(self):
        try:
            instance = postgres_sql_connect(**self.data)
            instance.set_client_encoding(self.__charset)

            return instance

        except PostgresSQLError:
            raise PostgresSQLDatabaseError(
                f'Connection to {self.name} Failed'
            )
      
    def __close(self, instance):
        try:
            instance.close() 
            
        except (AttributeError, PostgresSQLError):
            pass

    @property
    def name(self):
        return self.__name or str(self.data)

    def __str__(self):
        return self.name

class StorageController(ABC):
    '''
        Handles Store & Retrieve from Data Storage
    '''
    @abstractmethod
    def store(): # Return Command to fetch the data
        pass

    @abstractmethod
    def retrieve(): # Return Command to fetch the data
        pass

    @staticmethod
    def value_of(param: str, default, func: callable, *args, **kwargs):
        ''' determine if a param exists from given args, kwargs and return its value, otherwise return default'''
        return kwargs.get(param, StorageController.__value_of_arg(param, default, func, *args))

    @staticmethod
    def __value_of_arg(arg: str, default, func: callable, *args):
        try:
            index = getfullargspec(func).args.index(arg)

            assert(index >= 0) # Make sure we have a table arg

            return args[index]

        except (AssertionError, IndexError, KeyError, ValueError):
            return default

class DefaultStorageController(StorageController):
    '''
        Default Storage Controller, The default way to handle store & retrieve from Storage instance
    '''
    NUM_OF_KEYS = 10
    MAX_ROWS = 100000

    @staticmethod
    def __table_index(func: callable, *args, **kwargs):
        try:
            table_index = getfullargspec(func).args.index('table')
            
        except (IndexError, KeyError, ValueError):
            table_index = -1
        
        return table_index

    @staticmethod
    def __keys(func: callable, *args, **kwargs):
        key = digested_key(func, *args, **kwargs)

        keys = [f'{key}#{i}' for i in range(DefaultStorageController.NUM_OF_KEYS)]

        return keys

    @staticmethod
    def store(
        storage: redis.client.Redis, value: DataFrame, 
        func: callable, *args, 
        ttl=None, nx=True, **kwargs
    ):  
        keys = DefaultStorageController.__keys(func, *args, **kwargs)
        values = value.split(size=DefaultStorageController.MAX_ROWS) # This is a banner function
        
        for key, val in zip(keys, values):
            resp = storage.set(
                key, val.to_json(orient='records'), ex=ttl, nx=nx
            ) # set each value under key

            if not resp: 
                raise redis.ResponseError
            
        return True

    @staticmethod
    def retrieve(
        storage: redis.client.Redis, func: callable, *args, **kwargs
    ):
        keys = DefaultStorageController.__keys(func, *args, **kwargs)
        values = list(filter(None, storage.mget(keys)))

        table_index = DefaultStorageController.__table_index(func) # Is it a table query?

        df = DataFrame.from_dict(
            chain(*[loads(value) for value in values]), orient='columns'
        ).convert_dtypes()
        
        if table_index >= 0: # Should set df._tables
            table = kwargs.get('table') # Check if table kwarg exists

            if not table: # Else use arg
                table = args[table_index] # Will raise Index Error if missing
            
            df._tables = [table] # Set table metadata

        return df

class NewareCacheController(DefaultStorageController):
    '''
        Neware Cache Data(DataFrame) Storage Controller
        Handle store & retrieve for neware cache tables
    '''
    PRIMARY_KEY = ['ip', 'dev_uid', 'unit_id', 'chl_id', 'test_id'] # pk for cache table

    @staticmethod
    def __keys(func: callable, *args, **kwargs):
        ''' return keys arg from callable else return digested key'''
        _keys_index = NewareCacheController.__keys_index(func, *args, **kwargs)
        
        try:
            assert(_keys_index >= 0)
            
            if (all(isinstance(item, Iterable) for item in args[_keys_index])):
                _keys = [tuple(key) for key in args[_keys_index]] # Make sure each key(collection) is a tuple
            
            else:
                _keys = [tuple(args[_keys_index])] # Single entry was given
            
            return [
                f'{ip}-{device}-{unit}-{channel}-{test}' for ip, device, unit, channel, test in _keys
            ]
                
        except (AssertionError, TypeError):
            return digested_key(func, *args, **kwargs)
    
    @staticmethod
    def __keys_index(func: callable, *args, **kwargs):
        try:
            keys_index = getfullargspec(func).args.index('keys')

        except (IndexError, KeyError, ValueError):
            keys_index = -1

        return keys_index

    @staticmethod
    def __dump(df: DataFrame):
        df_without_pk = df[df.columns.difference(NewareCacheController.PRIMARY_KEY)]

        return {
            str(key): loads(value.to_json(orient='values')) for key, value in df_without_pk.items()
        }

    @staticmethod
    def __load(key: str, value: dict):
        df = DataFrame.from_dict(value)
        
        for pk, val in zip(reversed(NewareCacheController.PRIMARY_KEY), reversed(key.split('-'))):
            df.insert(0, pk, val)
        
        return df

    @staticmethod
    def __should_cache(condition: str, columns: list):
        ''' Determine if the query should be cached'''
        try: # More cases may appear, this can include all
            if condition and condition.lower() not in ['true', 1]: # Make sure condition doesnt create a partial result
                raise ValueError
            
            if set(columns) != NW_CACHE_COLUMNS: # Make sure we have all cache columns!
                raise ValueError

        except Exception as e:
            return False

        return True

    @staticmethod
    def store(
        storage: redis.client.Redis, value: DataFrame, 
        func: callable, *args, 
        ttl=None, nx=True, **kwargs
    ):
        kwargs = deepcopy(kwargs)
        condition = kwargs.get('condition', False)
        columns = kwargs.get('columns')

        if not columns or columns == '*':
            columns = value.columns

        if not NewareCacheController.__should_cache(condition, columns): # Partial value is given #TODO, should still be cached
            return DefaultStorageController.store(storage, value, func, *args, ttl=ttl, nx=nx, **kwargs) # use default since, since its a partial result

        try: 
            data = value.groupby(NewareCacheController.PRIMARY_KEY).apply(NewareCacheController.__dump)
            
            for key, val in data.items():
                _key = '-'.join(map(str, key))
                
                resp = storage.json().set(
                    _key, Path.root_path(), val, nx=nx
                ) # set each series by _key
                
                if resp:
                    storage.expire(_key, ttl) # if it was set, update ttl
                
            return True

        except (TypeError, KeyError, redis.ResponseError):
            raise
        
    @staticmethod
    def retrieve(
        storage: redis.client.Redis, func: callable, *args, **kwargs
    ):  
        kwargs = deepcopy(kwargs)
        condition = kwargs.get('condition', False)
        columns = kwargs.get('columns') # Requested columns

        if not columns or columns == '*':
            columns = NW_CACHE_COLUMNS

        if not NewareCacheController.__should_cache(condition, columns): # Partial value is given #TODO, value should be retrieved and completed!
            return DefaultStorageController.retrieve(storage, func, *args, **kwargs) # use default since, since its a partial result
        
        keys = NewareCacheController.__keys(func, *args, **kwargs) # Expected Keys
        
        try:
            values = storage.json().mget(keys, Path.root_path())
            values = list(filter(None, values)) # Remove Empty entries
            
            assert(len(values) == len(keys)) # make sure we have all values, #TODO more precise
            
            df = concat(
                [NewareCacheController.__load(key, value) for key, value in zip(keys, values)],
                ignore_index=True
            ) #into a df
            
            for column in df[NewareCacheController.PRIMARY_KEY].columns:
                df[column] = df[column].astype(int64) # All pk columns to type int

            for column in df.filter(like='time').columns:
                df[column] = df[column].astype('datetime64[ms]') # time columns into datetime
            
            return df[list(columns)].convert_dtypes()

        except (AssertionError, redis.ResponseError):
            return DataFrame()

class NewareTestController(NewareCacheController):
    '''
        Neware Test(DataFrame) Storage Controller
    '''
    VALUE_GROUP_KEY = 'cycle' # All df is a single test, is simply cycle
    
    @staticmethod
    def __dump(df: DataFrame):
        df_without_pk = df.drop(NewareTestController.VALUE_GROUP_KEY, axis=1)
        
        return {
            str(key): loads(value.to_json(orient='values')) for key, value in df_without_pk.items()
        }

    @staticmethod
    def __load(key: str, value: dict):
        df = DataFrame.from_dict(value)
        
        try:
            location = df.columns.get_loc("seq_id") + 1

        except KeyError:
            location = 0
    
        df.insert(location, NewareTestController.VALUE_GROUP_KEY, key)
        
        return df

    @staticmethod
    def __should_cache(cache_data: DataFrame, condition: str, raw: bool):
        try:
            assert(isinstance(cache_data, DataFrame)) # Must have cache df
            
            if not raw and condition and condition.lower() not in ['true', 1]:
                # Assumption!! If the given condition filters cache it will not contain partial cycle data, and is safe to use!
                # Any exception raised here means query is meant for value and should not be cached!
                
                # if len(cache_data.query(condition).index) == len(cache_data.index): 
                #     raise ValueError
                
                if not isinstance(cache_data.query(condition, engine='python'), DataFrame):
                    raise ValueError

        except Exception as e:
            return False

        return True

    @staticmethod
    def store(
        storage: redis.client.Redis, value: DataFrame, 
        func: callable, *args, 
        ttl=None, nx=True, **kwargs
    ):  
        kwargs = deepcopy(kwargs)
        cache_data, condition = kwargs.get('cache_data'), parse_mysql_to_pandas_query(kwargs.get('condition', ''))
        raw = kwargs.get('raw', False)
        
        if not NewareTestController.__should_cache(cache_data, condition, raw): # Partial value is given #TODO, should still be cached
            return DefaultStorageController.store(storage, value, func, *args, ttl=43200, nx=nx, **kwargs) # use default since, since its a partial result
        
        try: 
            partial_key = list(cache_data[NewareTestController.PRIMARY_KEY].iloc[-1]) # A single test so grab any(last) row
            
            data = value.groupby(NewareTestController.VALUE_GROUP_KEY).apply(NewareTestController.__dump) 
            
            for cycle, cycle_data in data.items(): 
                _key = f"{'-'.join(map(str, partial_key))}-{int(cycle)}"
                
                resp = storage.json().set(_key, Path.root_path(), {},  nx=nx) # Make sure Key exists

                if resp:
                    storage.expire(_key, ttl) # if it was set, update ttl
                
                for column, column_data in cycle_data.items(): # TODO with a single command (currently not implemented by redis)
                    if column in NW_CACHE_COLUMNS: # Case column belong to NW_CACHE_COLUMNS
                        column_data = column_data[0] # Only first value since neware_cache values are per cycle!
                        
                    resp = storage.json().set(
                        _key, Path(column), column_data, nx=nx
                    ) # set series by _key path
                        
            return True

        except (TypeError, KeyError, IndexError, UndefinedVariableError, redis.ResponseError):
            raise

    @staticmethod
    def retrieve(
        storage: redis.client.Redis, func: callable, *args, **kwargs
    ):  
        kwargs = deepcopy(kwargs)
        cache_data, condition = kwargs.get('cache_data'), parse_mysql_to_pandas_query(kwargs.get('condition', ''))
        raw = kwargs.get('raw', False) 
        temperature = kwargs.get('temperature', False)
        
        if not NewareTestController.__should_cache(cache_data, condition, raw): # Partial value is given #TODO, value should be retrieved and completed!
            return DefaultStorageController.retrieve(storage, func, *args, **kwargs) # use default since, since its a partial result
        
        try:
            if condition and condition.lower() not in ['true', 1]:
                cache_data = cache_data.query(condition, engine='python') # Only supports query on cache
            
            cycles = set(cache_data[NewareTestController.VALUE_GROUP_KEY]) # Ordered by default
            
            partial_key = list(cache_data[NewareTestController.PRIMARY_KEY].iloc[-1]) # A single test so grab any(last) row
            
            keys = [f"{'-'.join(map(str, partial_key))}-{cycle}" for cycle in cycles]
            
            values = storage.json().mget(keys, Path.root_path()) # grab all data
            
            values = list(filter(None, values)) # Remove Empty entries
            
            assert(len(values) == len(keys)) # TODO - HANDLE PARTIAL RESULT! (ONLY certain cycles in cache)
            
            df = concat(
                [NewareTestController.__load(cycle, value) for cycle, value in zip(cycles, values)],
                ignore_index=True
            ) # into df
            
            columns = kwargs.get('columns')
            
            if not isinstance(columns, list): # columns can be * (mysql all) or something invalid
                columns = df.columns

            if temperature:
                if cache_data['t1_max'].isnull().all() or cache_data['t2_max'].isnull().all(): # If a value exists in t1/t2_max - Temperature exists for the test!
                    assert(not df.filter(like='test_tmp').empty) # Since temperature exists, result should contain test_tmp columns
                    
                columns += [f'test_tmp{i+1}' for i in range(6)] # There are up to 6 temp channels
                
            df.loc[:,df.columns.isin(columns)]
            
            for column in df.filter(like='test_atime').columns: # Cast test columns to datetime
                df[column] = df[column].astype('datetime64[ms]')

            if kwargs.get('dqdv', False):
                # NOTE: As banner will become deprecated, leaving this as a temporary solution.
                # The dqdv calculation is done again since the window_length may vary
                df['dqdv'] = calculate_dqdv(df, raw=raw, window_length=kwargs.get('dqdv_smooth_filter', 21))  # Calculate dqdv

            return df.convert_dtypes()
            
        except (AssertionError, KeyError, IndexError, UndefinedVariableError, redis.ResponseError):
            return DataFrame()

class TableCacheController(DefaultStorageController):
    '''
        Store Tables Data(DataFrame) Storage Controller
    '''
    CACHED_TABLES = [
        'augm_per_cycle', 
        #'augm_per_cell', 'augm_per_test', 'augm_per_pulse', 'augm_per_anode',
        #'prediction_per_cycle_regressors', 'prediction_per_cycle_classifiers', 'prediction_per_cell',
        #'prediction_per_test', 'prediction_per_pulse', 'prediction_per_anode'
    ]
    
    
    @staticmethod
    def __should_cache(table: str, condition: str):
        try: # More cases may appear, this can include all
            if condition and condition.lower() not in ['true', 1]: # Make sure condition doesnt create a partial result
                raise ValueError
            
            if table not in TableCacheController.CACHED_TABLES: # Only certain tables (prediction and augment) are cached by TableCacheController
                raise ValueError

        except Exception as e:
            return False

        return True

    @staticmethod
    def store(
        storage: redis.client.Redis, value: DataFrame, 
        func: callable, *args, 
        ttl=None, nx=True, **kwargs
    ):
        condition = kwargs.get('condition', False)
        columns = kwargs.get('columns')

        if not columns or columns == '*':
            columns = value.columns

        try:
            table = value._tables[-1]

        except (KeyError, AttributeError):
            table = None

        if not TableCacheController.__should_cache(table, condition): # Partial value is given #TODO, value should be retrieved and completed!
            return DefaultStorageController.store(storage, value, func, *args, ttl=ttl, nx=nx, **kwargs)
        
        try:
            storage.json().set(table, Path.root_path(), {}, nx=True) # Make sure Key exists
            storage.expire(table, ttl)
            
            for column, series in value.items():
                _column = LABEL_TO_COLUMN.get(column, column)
                
                storage.json().set(
                    table, 
                    Path(_column), 
                    loads(series.to_json(orient='values')),
                    nx=nx
                )
                
            return True

        except (TypeError, KeyError, IndexError, UndefinedVariableError, redis.ResponseError):
            raise
        
    @staticmethod
    def retrieve(
        storage: redis.client.Redis, func: callable, *args, **kwargs
    ):  
        condition = TableCacheController.value_of('condition', False, func, *args, **kwargs)
        table = TableCacheController.value_of('table', None, func, *args, **kwargs)
        columns = TableCacheController.value_of('columns', None, func, *args, **kwargs)
        
        if not TableCacheController.__should_cache(table, condition): # Partial value is given #TODO, value should be retrieved and completed!
            return DefaultStorageController.retrieve(storage, func, *args, **kwargs)

        # objkeys
        try:
            if not columns: # Request did not specify columns
                columns = storage.json().objkeys(table, Path.root_path())
            
            data = storage.json().get(table, *columns)

            data = [Series(val, name=key) for key, val in data.items()]

            df = concat(data, axis=1)
            
            for column in df.filter(like='updated_on').columns:
                df[column] = df[column].astype('datetime64[ms]')
                
            return df.convert_dtypes()
        
        except (
            KeyError, IndexError, TypeError, 
            AttributeError, ValueError,
            UndefinedVariableError, redis.ResponseError
        ):
            return DataFrame()
        


QUERY_TO_STORAGE_CONTROL = dict(
    _neware_cache_query=NewareCacheController,
    neware_query=NewareTestController,
    table_query=TableCacheController,
) 