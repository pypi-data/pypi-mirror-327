from re import split
from typing import Union, Dict
from numbers import Number
from threading import Thread
from functools import wraps, partial
from collections.abc import Iterable
from collections import ChainMap
from datetime import datetime

import MySQLdb as mysql
from MySQLdb.cursors import DictCursor
from MySQLdb._exceptions import OperationalError, ProgrammingError
import pandas as pd
import numpy as np
from joblib import Parallel, delayed

from banner.utils.const import (
    FIRST_NEWARE_DATA_TABLE, SECOND_NEWARE_DATA_TABLE, FIRST_NEWARE_AUX_TABLE, SECOND_NEWARE_AUX_TABLE, 
    NW_TEMP, CACHE_CONNECTION_KWARG, TTL_KWARG, NW_DATA_SIGNIFICANT_COLUMNS, NW_AUX_SIGNIFICANT_COLUMNS,
    NW_AUX_CHANNEL, NW_UNIT, NW_CHANNEL, NW_TEST, NW_CYCLE, NW_SEQ, NW_STEP, NW_STEP_TYPE, NW_TIMESTAMP, 
    NW_VOLTAGE, NW_CURRENT, NW_STEP_RANGE, NX_KWARG
)
from banner.utils.neware import calculate_neware_columns, calculate_dqdv, merge_cache, query_cache
from banner.utils.web2py import (
    COLUMN_TO_LABEL as W2P_COLUMN_TO_LABEL, 
    LABEL_TO_COLUMN as W2P_LABEL_TO_COLUMN, 
    represent as w2p_repr, parse_w2p_to_mysql_query,
    experiments_to_sql, templates_to_sql,
    tests_to_sql, cells_to_sql
)
from banner.utils.misc import is_non_string_iterable, to_sql_range, key_value_to_string, to_list, query_df_by_dict
from banner.connection import Connection, Storage, RelationalConnection, MySqlConnection

class Queries(object): #TODO Statements
    @staticmethod
    def CONNECTIONS(conns: Dict[str, Connection] = {}):
        ''' 
            Dict of pre existing Connection Objects (name: connection)
            Setup new connections, returns all available
        '''
        try:
            Queries.CONNECTIONS.__CONNECTIONS.update(conns)

        except AttributeError:
            Queries.CONNECTIONS.__CONNECTIONS = {**conns}

        if not Queries.CONNECTIONS.__CONNECTIONS:
            return {None: None}

        return Queries.CONNECTIONS.__CONNECTIONS

    @staticmethod
    def CACHE(con: Storage = None):
        ''' 
            Sets a Storage Connection as default Cache
        '''
        try:
            assert(Queries.CACHE.__CACHE_CONNECTION)

        except (AssertionError, AttributeError):
            Queries.CACHE.__CACHE_CONNECTION = None

        if isinstance(con, Storage):
            Queries.CACHE.__CACHE_CONNECTION = con
        
        return Queries.CACHE.__CACHE_CONNECTION

    @staticmethod
    def __get_known_connection(connection: Union[Connection, str], typ: type = Connection):
        ''' Basicly an assertion for a given connection'''
        # If no connection is provided, grab first available
        if not connection:
            connections = [
                _connection for _connection in Queries.CONNECTIONS().values() if isinstance(_connection, typ)
            ]

            if not connections:
                raise IndexError('No Connections could be found')

            connection = connections[0]

        # Provided connection is not a Connection, is it a key?
        if not isinstance(connection, Connection):
            connection = Queries.CONNECTIONS().get(str(connection), connection)
        
        # No connection could be found
        if not isinstance(connection, Connection):
            raise KeyError(f'Unknown Connection', connection)

        if not isinstance(connection, typ):
            raise TypeError('Wrong Connection type', connection)

        return connection

    def __cache_query(value, cache: Storage, func: callable, args, ttl, nx, kwargs):
        ''' Handle caching of self(Queries) into provided cache'''
        try:
            assert(isinstance(cache, Storage))
            
            return cache.store(
                value, 
                func, 
                *args,
                ttl=ttl,
                nx=nx,
                **kwargs
            )

        except AssertionError:
            pass
        
        except Exception as e:
            exception_message = f'Failed Caching {func.__name__}:{args}{kwargs} into {cache} - {type(e).__name__}:{e}'
            print(exception_message) #TODO add flag for print(to stdout, which could be a provided log path)/exception
            # raise ValueError(message) from e
    
    def __cached_query(cache: Storage, func: callable, *args, **kwargs):
        ''' Get the cached value of Queries.func if exists inside provided cache'''
        try:
            assert(isinstance(cache, Storage))
            
            cached = cache.retrieve(
                func, *args, **kwargs
            )
            
            return cached

        except AssertionError:
            return pd.DataFrame()

    def __cache(func):
        ''' 
            Decorator for handling caching interaction, 
            A decorated Queries function will first check if its value exists in the provided cache,
            if exists -> return value
            if not exists -> calculate, cache and return value
        '''
        @wraps(func)
        def inner(*args, **kwargs):
            cache = kwargs.pop(CACHE_CONNECTION_KWARG, None)

            if cache is None: # Specifically checking for None, If False Do not cache!
                cache = Queries.CACHE() # None cache is provided, try to get the default one
            
            ttl = kwargs.pop(TTL_KWARG, None) # kwargs of the func
            nx = kwargs.pop(NX_KWARG, True) # args of the func
            
            value = Queries.__cached_query(cache, func, *args, **kwargs) # the cached value
            # TODO READ TYPE HINT FROM FUNC AND CHECK IF CACHE RESULT MATCHES TO SUPPORT ALL TYPE OF CACHING
            is_cached = True if isinstance(value, pd.DataFrame) and not value.empty else False
            
            if not is_cached or not nx: # value should be cached if it is not yet cached, or if nx=False (forcing a rewrite into cache)
                value = func(*args, **kwargs) # calculate the value
            
                # TODO Caching should be done using a suitable pkg (ex. CELERY)
                Thread(
                    target=Queries.__cache_query, 
                    kwargs=dict(
                        value=value,
                        cache=cache,
                        func=func,
                        args=args,
                        ttl=ttl,
                        nx=nx,
                        kwargs=kwargs
                    )
                ).start()
            
            return value
        
        return inner

    @staticmethod
    def __query(query: str, connection=None, cache=None, ttl=None, w2p_parse=True) -> pd.DataFrame:
        ''' direct str sql query without caching '''
        if not isinstance(query, str):
            return pd.DataFrame()

        connection = Queries.__get_known_connection(connection)
        
        if w2p_parse:
            query = parse_w2p_to_mysql_query(query)
        #TODO CHANGE TO LABELS?! NEEDS TO KNOW RAW
        return connection.retrieve(query)
    
    @staticmethod
    @__cache
    def simple_query(query: str, connection: Union[Connection, str] = None, cache: Storage = None, ttl: int = None, nx: bool = True, w2p_parse: bool = True) -> pd.DataFrame:
        '''
            Queries a given Connection/str of a known connection (or first known) return result as DataFrame
            Cache if cache or first known with ttl or default ttl for cache
            Raises KeyError and OperationalError
        '''
        return Queries.__query(
            query, 
            connection=connection, 
            cache=cache, 
            ttl=ttl, 
            w2p_parse=w2p_parse
        )

    @staticmethod
    def simple_edit(query: str, *args, connection: Union[Connection, str] = None, unique_checks=True, foreign_key_checks=True):
        '''
            Queries (Edit statements) a given Connection/str of a known connection (or first known)
            
            Raises KeyError and OperationalError
        '''
        connection = Queries.__get_known_connection(connection)
        
        return connection.store(query, *args, unique_checks=unique_checks, foreign_key_checks=foreign_key_checks)

    @staticmethod
    def delete_from(table: str, condition: str, connection: Union[Connection, str] = None):
        '''
            DELETE from table Statement by condition for a given connection
            
            Raises KeyError and OperationalError
        '''
        query = f"""
            DELETE FROM {table}
            WHERE {condition};
        """

        return Queries.simple_edit(query, connection=connection)

    @staticmethod
    def insert_update_into(table: str, **kwargs):
        '''
            INSERT INTO table Statement for a given connection(kwarg)
            If condition(kwarg) is present UPDATE instead
            Raises KeyError and OperationalError
        '''

        connection = kwargs.pop('connection', None)
        condition = kwargs.pop('condition', False)
        
        keys, values = map(str, kwargs.keys()), map(repr, kwargs.values())
        
        query = f"""
            UPDATE {table}
            SET {
                ', '.join([key_value_to_string(key, val) for key, val in zip(keys, values)])
            }
            WHERE {condition}; 
        """ if condition else f"""
            INSERT INTO {table} ({', '.join(keys)})
            VALUES ({', '.join(values)});
        """
        
        return Queries.simple_edit(query, connection=connection)

    @staticmethod
    def describe_table(table: str, connection: Union[RelationalConnection, str] = None) -> pd.DataFrame:
        '''
            Describes a table in connection
            Raises OperationalError and KeyError(Failed to find a connection for given key) 
        '''
        if not isinstance(table, str):
            return pd.DataFrame()

        connection = Queries.__get_known_connection(connection, RelationalConnection)
        
        data = connection.describe(table)
        
        data.insert(0, "Label", data['Field'].map(W2P_COLUMN_TO_LABEL)) # TODO W2P_COLUMN_TO_LABEL per table

        return data

    @staticmethod
    def describe(connection: Union[RelationalConnection, str] = None) -> pd.DataFrame:
        '''
            Describe Table names in connection
            Raises OperationalError and KeyError(Failed to find a connection for given key) 
        '''
        
        return Queries.__get_known_connection(connection, RelationalConnection).describe()

    @staticmethod
    @__cache
    def table_query(
        table: str, columns: Union[list, str] = '*', condition: str = 'TRUE', 
        connection: Union[RelationalConnection, str] = None, 
        represent: bool = False, raw: bool = False, 
        cache: Storage=None, ttl: int = None, nx: bool = True
    ) -> pd.DataFrame:
        '''
            Queries a given connection for 'SELECT {columns} FROM {table} WHERE {condition}'
            Accepts both column values and labels
            raw=True - column names as in db
            Queries a given Connection(ip)/str of a known connection (or first known) return result as DataFrame
            Cache if cache or first known with ttl or default ttl for cache
            Raises OperationalError and KeyError(Failed to find a connection for given key) 
        '''
        if isinstance(columns, str): # Handle columns as str
            columns = list(
                map(
                    str.strip,
                    filter(
                        None, 
                        split(
                            ' , |, | ,|,',
                            columns
                        )
                    )
                )
            )
        
        _columns = [W2P_LABEL_TO_COLUMN.get(column, column) for column in columns] # Get the actual column name (support Labels)
        
        data = Queries.__query(
            f"SELECT {', '.join(_columns)} FROM {table} WHERE {condition}",
            connection=connection,
            cache=cache,
            ttl=ttl
        )
        
        if not raw:
            try:
                #Columns as requested!
                data.columns = columns 

            except ValueError:
                # Case columns contain *
                data.columns = [W2P_COLUMN_TO_LABEL.get(column, column) for column in data.columns]
                pass
            
        data._tables = [table] # add _tables METADATA, indicating this dataframe represents a web2py table, allowing future joins
        
        if represent:
            data = w2p_repr(data) # Add column representation as they appear in web2py

        return data

    @staticmethod
    @__cache
    def neware_query(
        device: int, unit: int, channel: int, test: int, connection: Union[MySqlConnection, str] = None, 
        columns: Union[list, str] = [NW_UNIT, NW_CHANNEL, NW_TEST, NW_CYCLE, NW_SEQ, NW_STEP, NW_STEP_TYPE, NW_TIMESTAMP, NW_VOLTAGE, NW_CURRENT], 
        condition: str = 'TRUE', neware_condition: str = 'TRUE', raw: bool = False, dqdv: bool = False, temperature: bool = False,
        cache_data: pd.DataFrame = pd.DataFrame(), cache: Storage = None, ttl: int = None, dqdv_smooth_filter: int = 21
    ) -> pd.DataFrame:
        '''
            Queries a given Connection(ip)/str of a known connection (or first known) return result as DataFrame
            Cache if cache or first known with ttl or default ttl for cache
            If dqdv -> neware.calc_dq_dv
            Raises KeyError and OperationalError
        '''
        connection = Queries.__get_known_connection(connection, MySqlConnection)
        
        # Look for the tables
        try:
            neware_data = Queries.__query(
                f'SELECT * FROM h_test WHERE dev_uid = {device} AND unit_id = {unit} AND chl_id = {channel} AND test_id = {test}',
                connection=connection
            ).iloc[-1] # A single row is returned since we looked by primary key

            first_main_table = neware_data[FIRST_NEWARE_DATA_TABLE]
            first_aux_table = neware_data[FIRST_NEWARE_AUX_TABLE]

            second_main_table = neware_data[SECOND_NEWARE_DATA_TABLE] # May be None
            second_aux_table = neware_data[SECOND_NEWARE_AUX_TABLE] # May be None

        except IndexError:
            raise TypeError(f'{connection.name} has No data for device:{device}, unit:{unit}, channel:{channel}') 
        
        if isinstance(columns, str): # Determine what columns are requested
            columns = NW_DATA_SIGNIFICANT_COLUMNS if columns == '*' else to_list(columns)
        
        nw_columns = [column for column in columns if column in NW_DATA_SIGNIFICANT_COLUMNS] # Requested neware columns
        nw_cache_columns = [column for column in columns if column not in NW_DATA_SIGNIFICANT_COLUMNS] # Requested neware cache columns (only other source)
        
        try: # neware_cache contains the calculated cycle
            nw_cache_columns.append(
                nw_columns.pop(nw_columns.index(NW_CYCLE))
            )

        except ValueError: # Cycle was not requested
            pass
        
        if not nw_columns: # Case No neware columns were requested
            nw_columns.append(NW_SEQ) # Handle by appending seq_id
        
        # Parse W2P query
        condition = parse_w2p_to_mysql_query(condition)
        
        # Try to adjust query condition!
        if isinstance(cache_data, pd.DataFrame) and not cache_data.empty:
            try:
                condition = query_cache(
                    cache_data, str(condition)
                )
                
            except pd.core.computation.ops.UndefinedVariableError:
                pass
        
        required_columns = set([
            NW_SEQ, NW_TIMESTAMP, NW_STEP_RANGE, NW_VOLTAGE, NW_CURRENT, *nw_columns
        ]) # The actually needed columns (requested + required) 
        
        required_columns = ', '.join(required_columns) # to string
        
        first_data = Queries.__query(
            f'SELECT {required_columns} FROM {first_main_table} WHERE unit_id = {unit} AND chl_id = {channel} AND test_id = {test} AND ({condition} AND {neware_condition})', 
            connection=connection
        )

        second_data = Queries.__query(
            f'SELECT {required_columns} FROM {second_main_table} WHERE unit_id = {unit} AND chl_id = {channel} AND test_id = {test} AND ({condition} AND {neware_condition})', 
            connection=connection
        ) if second_main_table else pd.DataFrame() # There is a second main table for the test

        if temperature: # Temperature requested
            nw_aux_columns = ', '.join(NW_AUX_SIGNIFICANT_COLUMNS)

            if not first_data.empty: # If we have data in first_data then we will have from first_aux_table
                first_aux_data = Queries.__query(
                    f'SELECT {nw_aux_columns} FROM {first_aux_table} WHERE unit_id = {unit} AND chl_id = {channel} AND test_id = {test} AND ({condition} AND {neware_condition})', 
                    connection=connection
                )

                if not first_aux_data.empty:
                    first_data = pd.merge(first_data, first_aux_data, on=NW_SEQ) # Merge Aux from first_aux_table

            if second_aux_table and not second_data.empty: # There is a second aux table for the test and we have data in second_data then we will have from second_aux_table
                second_aux_data = Queries.__query(
                    f'SELECT {nw_aux_columns} FROM {second_aux_table} WHERE unit_id = {unit} AND chl_id = {channel} AND test_id = {test} AND ({condition} AND {neware_condition})', 
                    connection=connection
                )

                if not second_aux_data.empty:
                    second_data = pd.merge(second_data, second_aux_data, on=NW_SEQ) # Merge Aux from second_aux_table

        # Into a single Dataframe
        data = pd.concat([first_data, second_data], ignore_index=True)

        try:
            data = data.group_by_auxchl() # Banner method, neware.group_by_auxchl
            nw_columns.extend([column for column in data.columns if column.startswith(NW_TEMP)]) # nw_columns add temp columns
            
        except KeyError:
            pass
        
        if not raw:
            data = calculate_neware_columns(data, cache_df=cache_data) # Calculate neware columns

        if dqdv:
            data['dqdv'] = calculate_dqdv(data, raw=raw, window_length=dqdv_smooth_filter) # Calculate dqdv
            nw_columns.append('dqdv')

        try:
            data = merge_cache(data, cache_data, columns=nw_cache_columns) # Merge requested cache columns

        except KeyError:
            pass

        data = data[[*nw_columns, *nw_cache_columns]] # Keep requested columns
            
        return data
        
    @staticmethod
    def __neware_queries(
        devices: list, units: list, channels: list, tests: list, connection: Union[MySqlConnection, str] = None, 
        columns: Union[list, str] = [NW_UNIT, NW_CHANNEL, NW_TEST, NW_CYCLE, NW_SEQ, NW_STEP, NW_STEP_TYPE, NW_TIMESTAMP, NW_VOLTAGE, NW_CURRENT], 
        condition: str = 'TRUE', neware_condition: str = 'TRUE', temperature: bool = False, dqdv: bool = False, cache_data: pd.DataFrame = pd.DataFrame(),
        cache: Storage = None, ttl: int = None, raw: bool = False, dqdv_smooth_filter: int = 21
    ):  
        ''' This function gets multiple neware pks and their cache_data(df) calls neware_query per requested test with its relevant cache'''
        _connection_key = connection

        if isinstance(connection, Connection):
            _connection_key = str(_connection_key.name)

        data = dict()
        
        for device, unit, channel, test in zip(devices, units, channels, tests):
            try:
                data.update({
                    tuple([_connection_key, device, unit, channel, test]): Queries.neware_query(
                        device, unit, channel, test,
                        connection=connection,
                        cache=cache,
                        ttl=ttl,
                        raw=raw, 
                        dqdv=dqdv, 
                        condition=condition,
                        neware_condition=neware_condition,
                        columns=columns,
                        temperature=temperature,
                        dqdv_smooth_filter=dqdv_smooth_filter,
                        cache_data=cache_data[
                            (cache_data.dev_uid == int(device)) &
                            (cache_data.unit_id == int(unit)) & 
                            (cache_data.chl_id == int(channel)) & 
                            (cache_data.test_id == int(test))
                        ]
                    )
                })

            except (TypeError, KeyError, ValueError):
                pass #TODO ADD LOGGING
        
        return data

    @staticmethod
    def neware_cache_query(
        keys: Iterable, columns: Union[list, str] = '*', pulse: bool = False, anode: bool = False, condition: str = 'TRUE', 
        connection: Union[MySqlConnection, str] = None, cache: Storage = None, ttl: int = None
    ) -> pd.DataFrame:
        ''' 
            Query neware cache tables by iterable of keys, looking at neware_cache
            pulse flag on will look at neware_pulses_cache switching (removing the neware_cache entries) any pks found in the table into the result
            anode does the same as pulse with neware_cache_anode table
        '''
        neware_cache = Queries._neware_cache_query(
            keys, columns=columns, condition=condition, connection=connection, cache=cache, ttl=ttl
        ) # fetch neware_cache data
       
        neware_cache_pulse = Queries.neware_cache_pulse_query(
            keys, columns=columns, condition=condition, connection=connection, cache=cache, ttl=ttl
        ) if pulse else pd.DataFrame() # fetch neware_pulses_cache data

        neware_cache_pulse['pulse'] = 1 # It is a pulse

        neware_cache_anode = Queries.neware_cache_anode_query(
            keys, columns=columns, condition=condition, connection=connection, cache=cache, ttl=ttl
        ) if anode else pd.DataFrame() # fetch neware_cache_anode data
        
        neware_cache_anode['anode'] = 1 # It is an anode
        
        neware_cache = pd.concat(
            [neware_cache, neware_cache_pulse, neware_cache_anode], 
            ignore_index=True
        ) # Concat data
        
        def _keep_only_pulses(group):
            anodes = group[group['anode'] == 1]
            pulses = group[group['pulse'] == 1]
            default = group[(group['pulse'] != 1) & (group['anode'] != 1)]

            group = max([anodes, pulses, default], key=len)

            return group.drop(
                ['pulse','anode'], 
                axis=1, errors='ignore'
            )
        
        if neware_cache.empty:           
            return pd.DataFrame()
            
        neware_cache = neware_cache.groupby(
            ['ip', 'dev_uid', 'unit_id', 'chl_id', 'test_id'], as_index=False
        ).apply(_keep_only_pulses)
        
        if neware_cache.index.nlevels > 1:
            neware_cache = neware_cache.droplevel(0)

        return neware_cache
        
    @staticmethod
    @__cache
    def _neware_cache_query(
        keys: Iterable, columns: Union[list, str] = '*', condition: str = 'TRUE', connection: Union[MySqlConnection, str] = None,
        cache: Storage = None, ttl: int = None
    ) -> pd.DataFrame:
        ''' cache decorated __neware_cache_query for neware_cache table'''
        return Queries.__neware_cache_query(
            'neware_cache', keys, columns=columns, condition=condition, connection=connection, cache=cache, ttl=ttl
        )

    @staticmethod
    def neware_cache_anode_query(
        keys: Iterable, columns: Union[list, str] = '*', condition: str = 'TRUE', connection: Union[MySqlConnection, str] = None,
        cache: Storage = None, ttl: int = None
    ) -> pd.DataFrame:
        return Queries.__neware_cache_query(
            'neware_cache_anode', keys, columns=columns, condition=condition, connection=connection, cache=cache, ttl=ttl
        )

    @staticmethod
    def neware_cache_pulse_query(
        keys: Iterable, columns: Union[list, str] = '*', condition: str = 'TRUE', connection: Union[MySqlConnection, str] = None,
        cache: Storage = None, ttl: int = None
    ) -> pd.DataFrame:
        return Queries.__neware_cache_query(
            'neware_pulses_cache', keys, columns=columns, condition=condition, connection=connection, cache=cache, ttl=ttl
        )

    @staticmethod
    def __neware_cache_query(
        table: str, keys: Iterable, columns: Union[list, str] = '*', condition: str = 'TRUE', 
        connection: Union[MySqlConnection, str] = None, cache: Storage = None, ttl: int = None
    ) -> pd.DataFrame:
        '''
            Queries a given Connection(ip)/str of a known connection (or first known) return result as DataFrame
            Keys in the form (ip, device, unit, channel, test)
            Cache if cache or first known with ttl or default ttl for cache
            Raises KeyError and OperationalError
        '''
        connection = Queries.__get_known_connection(connection, MySqlConnection)

        if not isinstance(columns, str):
            columns = ','.join(columns)

        try:
            if (all(isinstance(item, Iterable) for item in keys)):
                _keys = [tuple(key) for key in keys] # Make sure each key(collection) is a tuple
                
            else:
                _keys = [tuple(keys)] # Single entry was given
            
            _keys = [
                f'({ip},{device},{unit},{channel},{test})' for ip, device, unit, channel, test in _keys
            ] # mysql entries

        except (TypeError, ValueError):
            raise ValueError(f'Bad Input, Expected List(Tuple)')
        
        _keys = f'(ip,dev_uid,unit_id,chl_id,test_id) IN ({",".join(_keys)})'
        
        if not isinstance(columns, str):
            columns = ','.join(columns)

        cache_data = Queries.__query(
            f"""
                SELECT {columns} FROM {table} 
                WHERE {_keys}
                AND {condition} 
            """,
            connection=connection
        )

        cache_data._tables = [table] # All table formats are the same!

        return cache_data

    @staticmethod
    def __neware_tests_query(
        table: str, experiments: str = '', templates: str = '', tests: str = '', cells: str = '', 
        columns: Union[list, str] = [NW_UNIT, NW_CHANNEL, NW_TEST, NW_CYCLE, NW_SEQ, NW_STEP, NW_STEP_TYPE, NW_TIMESTAMP, NW_VOLTAGE, NW_CURRENT],
        condition: str = 'TRUE', neware_condition: str = 'TRUE', raw: bool = False, dqdv: bool = False, temperature: bool = False, 
        connection: Union[MySqlConnection, str] = None, cache: Storage = None, ttl: int = None, dqdv_smooth_filter: int = 21
    ):  
        if not any([experiments, templates, tests, cells]):
            raise ValueError('A combination of experiments, templates, tests, cells is Required')
        
        connection = Queries.__get_known_connection(connection, MySqlConnection)

        __tests_query = f"""
            SELECT 
                {table}_test.ip, {table}_test.device, {table}_test.unit, {table}_test.channel, {table}_test.test_id
            FROM {table}
            LEFT JOIN {table}_test
            ON {table}.id = {table}_test.{table}_id
            LEFT JOIN {table}_test_template
            ON {table}_test.test_type_id = {table}_test_template.id
            WHERE 1
        """
        
        if experiments and isinstance(experiments, str):
            __tests_query += f' AND {experiments}'
        
        if templates and isinstance(templates, str):
            __tests_query += f' AND {templates}'

        if tests and isinstance(tests, str):
            __tests_query += f' AND {tests}'

        if cells and isinstance(cells, str):
            __tests_query += f' AND {cells}'
        
        __tests = Queries.__query(
            __tests_query,
            connection=connection,
            cache=cache,
            ttl=ttl
        ).dropna()
        
        if __tests.empty:
            return {}

        # Make sure all data is numeric
        __tests = __tests.astype(int, errors='ignore')
        
        __cached_data = Queries.neware_cache_query(
            list(__tests.itertuples(index=False, name=None)),
            pulse=True, anode=True,
            connection=connection, 
            #cache=cache, ttl=ttl
        )
        
        __tests_by_ip = __tests.groupby('ip')
        
        data = Parallel(n_jobs=__tests_by_ip.ngroups, require='sharedmem', verbose=0)(
            delayed(Queries.__neware_queries)(
                df['device'].values, df['unit'].values, df['channel'].values, df['test_id'].values,
                connection=name, cache=cache, ttl=ttl, raw=raw, columns=columns,
                dqdv=dqdv, condition=condition, neware_condition=neware_condition, temperature=temperature,
                dqdv_smooth_filter=dqdv_smooth_filter, cache_data=__cached_data[__cached_data.ip == int(name)]
            )
            for name, df in __tests_by_ip
        )
        
        return dict(ChainMap(*data))

    @staticmethod
    def neware_tests_query(
        table: str, experiments: Union[list, Number, str] = [], templates: Union[list, Number, str] = [], 
        tests: Union[list, Number, str] = [], cells: Union[list, Number, str] = [], 
        columns: Union[list, str] = [NW_UNIT, NW_CHANNEL, NW_TEST, NW_CYCLE, NW_SEQ, NW_STEP, NW_STEP_TYPE, NW_TIMESTAMP, NW_VOLTAGE, NW_CURRENT], 
        condition: str = 'cycle < 2', neware_condition: str = 'TRUE', raw: bool = False, dqdv: bool = False, temperature: bool = False,
        connection: Union[MySqlConnection, str] = None, cache: Storage = None, ttl: int = None, dqdv_smooth_filter: int = 21
    ):
        if not any([experiments, templates, tests, cells]):
            raise ValueError('A combination of experiments, templates, tests, cells is Required')
        
        experiments = experiments_to_sql(table, experiments)
        templates = templates_to_sql(f'{table}_test_template', templates)
        cells = cells_to_sql(table, cells)
        tests = tests_to_sql(f'{table}_test', tests)
         
        return Queries.__neware_tests_query(
            table, experiments, templates, 
            tests, cells, columns, condition, neware_condition, raw, 
            dqdv, temperature, connection, cache, ttl, dqdv_smooth_filter
        )
    
    @staticmethod
    @__cache
    def test_tables_query(
        table: str, experiments: Union[list, Number, str] = [], templates: Union[list, Number, str] = [], 
        tests: Union[list, Number, str] = [], cells: Union[list, Number, str] = [], 
        connection: Union[MySqlConnection, str] = None, cache: Storage = None, ttl: int = None
    ):
        # return df of ip dev etc + testid + cell + cache tables x3 + neware tables x4
        if not any([experiments, templates, tests, cells]):
            raise ValueError('A combination of experiments, templates, tests, cells is Required')
        
        experiments = experiments_to_sql(table, experiments)
        templates = templates_to_sql(f'{table}_test_template', templates)
        cells = cells_to_sql(table, cells)
        tests = tests_to_sql(f'{table}_test', tests)

        condition = ' AND '.join(
            filter(None, [experiments, templates, cells, tests])
        )
        
        __tests_query = f"""
            SELECT 
                {table}_test.id, {table}_test.ip, {table}_test.device, {table}_test.unit, {table}_test.channel, {table}_test.test_id
            FROM {table}
            LEFT JOIN {table}_test
            ON {table}.id = {table}_test.{table}_id
            LEFT JOIN {table}_test_template
            ON {table}_test.test_type_id = {table}_test_template.id
            WHERE {condition}
        """

        __data = Queries.simple_query(
            __tests_query,
            connection=connection,
            cache=cache,
            ttl=ttl
        ).dropna()

        if __data.empty:
            return __data

        keys = ['device', 'unit', 'channel', 'test_id']
        neware_keys = ['dev_uid', 'unit_id', 'chl_id', 'test_id']
        neware_keys_as_str = ', '.join(neware_keys)

        def __query_h_test(group):
            values = [str(tpl) for tpl in group[keys].itertuples(index=False, name=None)]
            condition = f"({neware_keys_as_str}) IN ({', '.join(values)})"
            
            h_test = Queries.__query(
                f"""
                    SELECT {neware_keys_as_str}, {FIRST_NEWARE_DATA_TABLE}, {SECOND_NEWARE_DATA_TABLE}, {FIRST_NEWARE_AUX_TABLE}, {SECOND_NEWARE_AUX_TABLE}
                    FROM h_test WHERE {condition}
                """,
                connection=group.name
            ) # Select relevant data from h_test of neware (group.name)

            if not h_test.empty:
                h_test['ip'] = group.name

            return h_test
        
        __data = __data.apply(pd.to_numeric) # Ensure all columns are numeric, device column might be string
        __h_test_data = __data.groupby('ip').apply(__query_h_test).reset_index(drop=True) # Add neware tables
        
        keys.insert(0 , 'ip')
        neware_keys.insert(0 , 'ip')
        
        if not __h_test_data.empty:
            __data = __data.merge(
                __h_test_data,
                left_on=keys,
                right_on=neware_keys
            ) # Merge h_test into group
            
        values = [tpl for tpl in __data[keys].itertuples(index=False, name=None)]

        # Set cache tables to False
        __data.assign(
            neware_cache=False, neware_pulses_cache=False, neware_cache_anode=False
        )
        
        neware_cache = Queries.neware_cache_query(values, columns=neware_keys, condition='cycle <= 1') # Only single row per test

        if not neware_cache.empty:
            neware_cache['neware_cache'] = True

            __data = __data.merge(
                neware_cache,
                left_on=keys,
                right_on=neware_keys,
                how='left'
            ) # Merge neware_cache

            __data['neware_cache'].replace(to_replace=np.nan, value=False, inplace=True)
        
        neware_cache_pulse = Queries.neware_cache_pulse_query(values, columns=neware_keys, condition='cycle <= 1') # Only single row per test

        if not neware_cache_pulse.empty:
            neware_cache_pulse['neware_pulses_cache'] = True

            __data = __data.merge(
                neware_cache_pulse,
                left_on=keys,
                right_on=neware_keys,
                how='left'
            ) # Merge neware_cache_pulse

            __data['neware_pulses_cache'].replace(to_replace=np.nan, value=False, inplace=True)
        
        neware_cache_anode = Queries.neware_cache_anode_query(values, columns=neware_keys, condition='cycle <= 1') # Only single row per test

        if not neware_cache_anode.empty:
            neware_cache_anode['neware_cache_anode'] = True

            __data = __data.merge(
                neware_cache_anode,
                left_on=keys,
                right_on=neware_keys,
                how='left'
            ) # Merge neware_cache_anode

            __data['neware_cache_anode'].replace(to_replace=np.nan, value=False, inplace=True)
        
        return __data[__data.columns.intersection([
            'id', *keys, 'neware_cache', 'neware_pulses_cache', 'neware_cache_anode',
            FIRST_NEWARE_DATA_TABLE, SECOND_NEWARE_DATA_TABLE, FIRST_NEWARE_AUX_TABLE, SECOND_NEWARE_AUX_TABLE
        ])]


class AugmentQueries(object):
    # available table keys
    PER_CYCLE_TABLE = 'augm_per_cycle'
    PER_CYCLE_SNAPPER_TABLE = 'augm_per_cycle_snapper'
    PER_CELL_TABLE = 'augm_per_cell'
    PER_TEST_TABLE = 'augm_per_test'
    PER_PULSE_TABLE = 'augm_per_pulse'
    PER_ANODE_TABLE = 'augm_per_anode'

    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S" # web2py timestamp format

    COLUMN_DESCRIPTION_INDEX = '_description' # description column suffix
    COLUMN_UPDATED_ON_INDEX = '_updated_on' # index column suffix

    PER_CELL_UNIQUE_COLUMNS = ['cell_table', 'cell_id'] # Unique columns (pk) per cell table
    PER_TEST_UNIQUE_COLUMNS = ['augm_per_cell', 'test_id'] # Unique columns (pk) per test table
    PER_CYCLE_UNIQUE_COLUMNS = ['augm_per_test', 'ip', 'dev_uid', 'unit_id', 'chl_id', 'test_id', 'cycle'] # Unique columns (pk) per cycle table

    def __init__(self, connection: RelationalConnection):
        # set instance values
        self._connection = connection

        self.prefix = 'augm'

        self.per_cycle_table = AugmentQueries.PER_CYCLE_TABLE
        self.per_cell_table = AugmentQueries.PER_CELL_TABLE
        self.per_test_table = AugmentQueries.PER_TEST_TABLE
        self.per_pulse_table = AugmentQueries.PER_PULSE_TABLE
        self.per_anode_table = AugmentQueries.PER_ANODE_TABLE

        self.tables = (
            self.per_cycle_table,
            self.per_cell_table,
            self.per_test_table,
            self.per_pulse_table,
            self.per_anode_table
        )

        self.associated_cache_tables = {
            self.per_cycle_table: 'neware_cache',
            self.per_pulse_table: 'neware_pulses_cache',
            self.per_anode_table: 'neware_cache_anode',
        }
        
        self.required_columns_for_table = {
            self.per_cycle_table: AugmentQueries.PER_CYCLE_UNIQUE_COLUMNS,
            self.per_pulse_table: AugmentQueries.PER_CYCLE_UNIQUE_COLUMNS,
            self.per_anode_table: AugmentQueries.PER_CYCLE_UNIQUE_COLUMNS,
            self.per_cell_table: AugmentQueries.PER_CELL_UNIQUE_COLUMNS,
            self.per_test_table: AugmentQueries.PER_TEST_UNIQUE_COLUMNS,
        }

        self.primary_columns = ['cell_table', 'cell_id', 'test_id', 'cycle']

    def __assert_table(self, table: str):
        if table not in self.tables:
            raise ValueError(f'Available {self.__class__.__name__} Tables: {self.tables}')
    
    def get_keys_per_table(self, data: pd.DataFrame, table: str):
        columns = self.required_columns_for_table.get(table)
        
        return [str(tuple(row)) for _, row in data[columns].iterrows()]
 
    def set_features(self, table: str, features: pd.DataFrame, columns: list, validate=True): # TABLE, CELL, TEST_ID, CYCLE 
        ''' Given a features df, set/update columns'''
        # Only keep required columns + columns
        self.__assert_table(table)

        _columns = self.primary_columns + columns
        
        features = features[features.columns.intersection(set(_columns))]
        
        if validate:
            features = self.__filter_non_existant(table, features) # make sure pks are valid 
        
        keys = self.get_keys_per_table(features, self.per_cell_table) # table pks per cell
        
        self.__create_rows_per_table(keys, self.per_cell_table) # Create Per Cell Rows!
        
        features = features.merge(
            self.__get_per_table_rows(keys, self.per_cell_table), # Relevant Rows
            how='left', on=self.required_columns_for_table.get(self.per_cell_table)
        ) # Add params
        
        if table != self.per_cell_table: # Tests/Cycles/Pulses/Anode
            keys = self.get_keys_per_table(features, self.per_test_table) # table pks per cell
            
            self.__create_rows_per_table(keys, self.per_test_table) # Create Per Test Rows!
            
            features = features.merge(
                self.__get_per_table_rows(keys, self.per_test_table), # Relevant Rows
                how='left', 
                on=self.required_columns_for_table.get(self.per_test_table)
            ) # Add params
            
            if table != self.per_test_table: # Cycles/Pulses/Anode
                features = self.__create_and_get_rows_per_cycle_pulse_or_anode(features, table)
                
        for part in features.split(): # Banner function 
            self.__set_feature(table, part, columns) # Set feature into table
        
    def add_feature(self, table: str, name: str, dtype: str, index=False, description=False, updated_on=False):
        ''' 
            Add a new column to the db(self._connection)
            Set column as index if True,
            Add column_description if True,
            Add column_updated_on if True
        '''
        self.__assert_table(table)
        
        self.__add_column(table, name, dtype)

        if index:
            self.__add_index(table, name)

        if description:
            self.__add_column(table, f'{str(name)}{self.COLUMN_DESCRIPTION_INDEX}', 'VARCHAR(255)')

        if updated_on:
            self.__add_column(table, f'{str(name)}{self.COLUMN_UPDATED_ON_INDEX}', 'DATETIME')

    def __add_column(self, table: str, name: str, dtype: str):
        Queries.simple_edit(
            f'ALTER TABLE {table} ADD COLUMN {str(name)} {str(dtype)}',
            connection=self._connection
        )

    def __add_index(self, table: str, name: str):
        Queries.simple_edit(
            f'ALTER TABLE {table} ADD INDEX ({str(name)})',
            connection=self._connection
        )

    def __get_per_table_rows(self, keys: Iterable, table: str):
        columns = ','.join(self.required_columns_for_table.get(table))
        condition = f'({columns}) IN ({",".join(keys)})'
        
        return Queries.simple_query(
            f"""
                SELECT id as {table}, {columns}
                FROM {table} 
                WHERE {condition}
            """,
            connection=self._connection
        )

    def __create_rows_per_table(self, keys: Iterable, table: str):
        columns = self.required_columns_for_table.get(table)
        on_duplicate = [f'{column}=VALUES({column})' for column in columns]
        
        Queries.simple_edit(
            f"""
                INSERT INTO {table} ({",".join(columns)}) 
                VALUES {",".join(keys)}
                ON DUPLICATE KEY
                UPDATE {",".join(on_duplicate)};
            """,
            connection=self._connection
        )

    def __set_feature(self, table: str, features: pd.DataFrame, columns: list):
        ''' Actual function to update the rows '''
        if not columns or features.empty:
            return
        
        columns = list(columns)
        
        _columns = [*self.required_columns_for_table.get(table), *columns]
        
        _features = features[_columns] # augm_per_test requires id!
        
        table_description = Queries.describe_table(table, connection=self._connection) # description of the table
        
        updated_on_columns = list()

        for column in columns:
            # Set updated_on for column
            if (column_updated_on_index := f'{column}{AugmentQueries.COLUMN_UPDATED_ON_INDEX}') in table_description.Field.values:
                updated_on_columns.append(column_updated_on_index)
        
        _features = _features.assign(**{
            column: datetime.now().strftime(AugmentQueries.TIMESTAMP_FORMAT) for column in updated_on_columns
        }) # with updated_on
        
        columns.extend(updated_on_columns)

        values = tuple(
            tuple(row) for row in _features.values.tolist() # Iterate every row
        )
        placeholders = ','.join('%s' for val in values)

        columns_as_str = ', '.join(_features.columns)
        
        on_duplicate = [f'{column}=VALUES({column})' for column in columns]

        query = f"INSERT INTO {table} ({columns_as_str}) VALUES {placeholders} ON DUPLICATE KEY UPDATE {','.join(on_duplicate)};"
        
        Queries.simple_edit(
            query, values, connection=self._connection
        )

    def __create_and_get_rows_per_cycle_pulse_or_anode(self, data: pd.DataFrame, table: str):
        cache_table = self.associated_cache_tables[table]
        cache_kwargs = dict(anode=True, pulse=True) if cache_table == 'neware_cache' else {}
        columns = ['ip', 'dev_uid', 'unit_id', 'chl_id', 'test_id', 'cycle']
        cache_columns = {f'{cache_table}.{column}': column for column in columns}
        
        def __create_augm_per_pk(group):
            test_table = f'{group.name}_test'
            
            try:
                data = Queries.table_query(
                    test_table, raw=True,
                    columns=['id', 'ip', 'device', 'unit', 'channel', 'test_id'], 
                    condition=f"id IN ({', '.join(group['test_id'].astype(str))})"
                ).join_table(
                    cache_table, columns=columns,
                    **cache_kwargs
                )

                group['cycle'] = group['cycle'].astype('Int64')
                data[f'{cache_table}.cycle'] = data[f'{cache_table}.cycle'].astype('Int64')

                joined_group = group.merge(data, how='inner', left_on=['test_id', 'cycle'], right_on=[f'{test_table}.id', f'{cache_table}.cycle'])
                joined_group[f'{cache_table}.dev_uid'] = pd.to_numeric(joined_group[f'{cache_table}.dev_uid']) # device is originally a string
                joined_group.drop(columns, inplace=True, axis=1, errors='ignore')
                joined_group.rename(columns=cache_columns, inplace=True)
                
            except TypeError:
                joined_group = pd.DataFrame()
            
            if joined_group.empty:
                return joined_group

            required_columns = self.required_columns_for_table.get(table)
            on_duplicate = [f'{column}=VALUES({column})' for column in required_columns]

            values = [str(tpl) for tpl in joined_group[required_columns].itertuples(index=False, name=None)]
            values_as_string = ", ".join(values)
            
            # Set rows
            Queries.simple_edit(
                f"""
                    INSERT INTO {table} ({",".join(required_columns)}) 
                    VALUES {values_as_string}
                    ON DUPLICATE KEY
                    UPDATE {",".join(on_duplicate)};
                """,
                connection=self._connection
            )
            
            _data = Queries.simple_query(
                f'SELECT id, {",".join(required_columns)} FROM {table} WHERE ({",".join(required_columns)}) IN ({values_as_string})',
                connection=self._connection
            )
            
            return joined_group.merge(
                _data, how='inner', 
                on=required_columns
            )
        
        return data.groupby('cell_table').apply(__create_augm_per_pk)

    def __filter_non_existant(self, table: str, data: pd.DataFrame):
        def __filter_by_cells(group):
            condition=f"id IN ({', '.join(group['cell_id'].astype(str))})"

            valid_ids = Queries.table_query(
                group.name, condition=condition, columns='id'
            )
            
            if valid_ids.empty:
                return valid_ids

            return group.merge(valid_ids, how='right', left_on='cell_id', right_on='id')

        def __filter_by_tests(group):
            query_table = f'{group.name}_test'
            
            values = [str(tpl) for tpl in group[['test_id', 'cell_id']].itertuples(index=False, name=None)]
            condition = f"(id, {group.name}_id) IN ({', '.join(values)})"
            
            valid_ids = Queries.table_query(
                query_table, condition=condition, columns='id'
            )

            if valid_ids.empty:
                return valid_ids

            return group.merge(valid_ids, how='right', left_on='test_id', right_on='id')

        filter_func = __filter_by_cells if table == self.per_cell_table else __filter_by_tests

        return data.groupby('cell_table', as_index=False).apply(filter_func)

class PredictionQueries(AugmentQueries):
    PER_CYCLE_REGRESSORS_TABLE = 'prediction_per_cycle_regressors'
    PER_CYCLE_CLASSIFIERS_TABLE = 'prediction_per_cycle_classifiers'
    PER_CELL_TABLE = 'prediction_per_cell'
    PER_TEST_TABLE = 'prediction_per_test'
    PER_PULSE_TABLE = 'prediction_per_pulse'
    PER_ANODE_TABLE = 'prediction_per_anode'
    PREDICTOR_TABLE = 'predictor'

    PER_CELL_UNIQUE_COLUMNS = ['cell_table', 'cell_id', 'predictor'] # Unique columns (pk) per cell table
    PER_TEST_UNIQUE_COLUMNS = ['prediction_per_cell', 'test_id', 'predictor'] # Unique columns (pk) per test table
    PER_CYCLE_UNIQUE_COLUMNS = ['prediction_per_test', 'ip', 'dev_uid', 'unit_id', 'chl_id', 'test_id', 'cycle', 'predictor'] # Unique columns (pk) per cycle table

    def __init__(self, connection: RelationalConnection):
        self._connection = connection

        self.prefix = 'prediction'

        self.per_cycle_regressors_table = PredictionQueries.PER_CYCLE_REGRESSORS_TABLE
        self.per_cycle_classifiers_table = PredictionQueries.PER_CYCLE_CLASSIFIERS_TABLE
        
        self.per_cell_table = PredictionQueries.PER_CELL_TABLE
        self.per_test_table = PredictionQueries.PER_TEST_TABLE
        self.per_pulse_table = PredictionQueries.PER_PULSE_TABLE
        self.per_anode_table = PredictionQueries.PER_ANODE_TABLE
        self.predictor_table = PredictionQueries.PREDICTOR_TABLE

        self.tables = (
            self.per_cycle_regressors_table,
            self.per_cycle_classifiers_table,
            self.per_cell_table,
            self.per_test_table,
            self.per_pulse_table,
            self.per_anode_table,
            self.predictor_table
        )

        self.associated_cache_tables = {
            self.per_cycle_regressors_table: 'neware_cache',
            self.per_cycle_classifiers_table: 'neware_cache',
            self.per_pulse_table: 'neware_pulses_cache',
            self.per_anode_table: 'neware_cache_anode',
        }

        self.required_columns_for_table = {
            self.per_cycle_regressors_table: PredictionQueries.PER_CYCLE_UNIQUE_COLUMNS,
            self.per_cycle_classifiers_table: PredictionQueries.PER_CYCLE_UNIQUE_COLUMNS,
            self.per_pulse_table: PredictionQueries.PER_CYCLE_UNIQUE_COLUMNS,
            self.per_anode_table: PredictionQueries.PER_CYCLE_UNIQUE_COLUMNS,
            self.per_cell_table: PredictionQueries.PER_CELL_UNIQUE_COLUMNS,
            self.per_test_table: PredictionQueries.PER_TEST_UNIQUE_COLUMNS,
        }

        self.primary_columns = ['cell_table', 'cell_id', 'test_id', 'cycle', 'predictor']

        self.unique_columns = ['name', 'version']

        self.model_column = 'model'

    def set_update_predictors(self, predictors: pd.DataFrame):
        ''' Predictor table has a blob type column, model, which requires special handling '''
        predictor_columns = Queries.describe_table('predictor', connection=self._connection)['Field'].values

        _predictors = predictors[predictors.columns.intersection(set(predictor_columns))] # Intersection of given columns with available columns
        
        _predictors = _predictors.loc[:,~_predictors.columns.str.endswith('updated_on')] # updated_on columns should not be set manually
        
        updated_on_columns = list() # list of updated_on columns

        # Find if a column has an updated_on column
        for column in _predictors.columns:
            if (column_updated_on_index := f'{column}{PredictionQueries.COLUMN_UPDATED_ON_INDEX}') in predictor_columns:
                updated_on_columns.append(column_updated_on_index)
                
        _predictors = _predictors.assign(**{
            column: datetime.now().strftime(AugmentQueries.TIMESTAMP_FORMAT) for column in updated_on_columns
        }) # Add updated_on column
        
        if self.model_column in predictors:
            _predictors.drop(self.model_column, inplace=True, axis=1) # model is a glob(binary) column, it is handled by itself

        on_duplicate = [f'{column}=VALUES({column})' for column in _predictors.columns] # How to handle duplicate
        
        keys = [str(tuple(row)) for _, row in _predictors.iterrows()] # as mysql tuples
        
        Queries.simple_edit(
            f"""
                INSERT INTO {self.predictor_table} ({",".join(_predictors.columns)}) 
                VALUES {",".join(keys)}
                ON DUPLICATE KEY
                UPDATE {",".join(on_duplicate)};
            """,
            connection=self._connection
        ) # Insert/Update
        
        if self.model_column in predictors: # handle model column
            for _, row in predictors[[*self.unique_columns, self.model_column]].iterrows():
                name, version = row[self.unique_columns]
                model = row[self.model_column]
                
                Queries.simple_edit(
                    """UPDATE predictor SET model=%s WHERE name=%s AND version=%s""" , (model, name, version),
                    connection=self._connection
                ) # Update since rows should exist by now