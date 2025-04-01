# https://github.com/pandas-profiling/pandas-profiling/blob/develop/src/pandas_profiling/controller/pandas_decorator.py
# https://github.com/scls19fr/pandas-helper-calc/blob/master/pandas_helper_calc/__init__.py
"""This file add the decorator on the DataFrame object."""

from collections.abc import Iterable
from typing import Union, Dict

from pandas import DataFrame
from MySQLdb import MySQLError

from banner.connection import RelationalConnection, Storage
from banner.queries import Queries

from banner.utils.web2py import JOINS, COLUMN_TO_LABEL
from banner.utils.misc import to_mysql_tuple
from banner.utils.pandas import assert_required_columns
from banner.utils.neware import (
    calculate_current, calculate_dqdv, calculate_neware_columns, 
    calculate_neware_timestamp, calculate_temperature, calculate_neware_datetime,
    calculate_voltage, group_by_auxchl, calculate_capacity, IS_CALCULATED_NEWARE_DF
)

def __split(df: DataFrame, size=100000):
    '''
        Split DataFrame into chunk_size list of DataFrames
    '''    
    return [df[i*size:(i+1)*size] for i in range(len(df) // size + 1)]

def __slope(df: DataFrame, x:str, y:str):
    '''
        Calculate Delta Y / Delta X
    '''
    return df[y].diff() / df[x].diff()
    
DataFrame.split = __split
DataFrame.slope = __slope

# Neware functions
DataFrame.calculate_current = calculate_current
DataFrame.calculate_neware_timestamp = calculate_neware_timestamp
DataFrame.calculate_temperature = calculate_temperature
DataFrame.calculate_voltage = calculate_voltage
DataFrame.calculate_neware_columns = calculate_neware_columns
DataFrame.calculate_dq_dv = calculate_dqdv
DataFrame.group_by_auxchl = group_by_auxchl
DataFrame.calculate_capacity = calculate_capacity
DataFrame.calculate_neware_datetime = calculate_neware_datetime
DataFrame.IS_CALCULATED_NEWARE_DF = IS_CALCULATED_NEWARE_DF


# Wrapper around Queries.table_query
def __join_table(
    df: DataFrame, table: str, columns: Union[list, str] = '*', condition: str = 'TRUE',
    left: Union[str, list, None] = None, right: Union[str, list, None] = None, how: Union[str, None] = None,
    connection: Union[RelationalConnection, str] = None, represent: bool = False,
    raw: bool = False, cache: Storage=None, ttl: Union[bool, None] = None, nx: bool = True,
    **kwargs
):
    ''' 
        Join a df representing web2py table rows with another web2py table 
    '''
    _df = df.copy()
    
    try:
        assert(isinstance(df._tables, list)) # Is a list
        assert(df._tables) # Is not empty
 
    except (AssertionError, AttributeError):
        raise TypeError('DataFrame Does not represent a StoreDot Table')
    
    if len(df._tables) == 1: #First Join
        _df.columns = [f'{df._tables[0]}.{column}' for column in _df.columns] # Prefix columns

    for df_table in df._tables: # Iterate available tables
        join_params = JOINS.get(df_table, dict()).get(table, dict())

        _how = how if how else join_params.get('how') # how the join should be performed
        _left = left if left else join_params.get('left') # left keys
        _right = right if right else join_params.get('right') # right keys
        
        if not all([_left, _right, _how]):
            continue
        
        if not isinstance(_left, list):
            _left = [_left] # a single value was given
    
        if not isinstance(_right, list):
            _right = [_right] # a single value was given
        
        _left = [
            f'{df_table}.{column}' if f'{df_table}.{column}' in _df else f'{df_table}.{COLUMN_TO_LABEL.get(column)}'
            for column in _left
        ] #Add table prefix
        
        try:
            _keys = _df[_left].dropna() # Keys cannot contain NA values
            _keys = zip(*[_keys[column].values for column in _left]) # as Iterable
            # the neware cache tables contain only numeric values
            # Cache tables are a special case
            if table == 'neware_cache':
                table_df = Queries.neware_cache_query(
                    list(_keys), columns=columns, condition=condition, 
                    connection=connection, cache=cache, ttl=ttl,
                    **kwargs
                )

            elif table == 'neware_pulses_cache':
                table_df = Queries.neware_cache_pulse_query(
                    list(_keys), columns=columns, condition=condition, 
                    connection=connection, ttl=ttl,
                    **kwargs
                )
                
            elif table == 'neware_cache_anode':
                table_df = Queries.neware_cache_anode_query(
                    list(_keys), columns=columns, condition=condition, 
                    connection=connection, ttl=ttl,
                    **kwargs
                )

            else:
                # keys may contain str values
                _keys = [to_mysql_tuple(values) for values in _keys] # as Iterable of strings
                
                table_df = Queries.table_query(
                    table, columns=columns, condition=f"({','.join(_right)}) IN ({','.join(_keys)}) AND {condition}",
                    represent=represent, raw=raw, connection=connection, cache=cache, ttl=ttl, nx=nx, **kwargs
                ) # for any other table use table_query
            
            table_df.columns = [f'{table}.{column}' for column in table_df.columns] # Prefix columns
            
            _right = [
                f'{table}.{column}' if f'{table}.{column}' in table_df else f'{table}.{COLUMN_TO_LABEL.get(column)}'
                for column in _right
            ] #Add table prefix
            
            tables = df._tables + [table] # the resulting tables metadata
            
            for left_column, right_column in zip(_left, _right):
                table_df[right_column] = table_df[right_column].astype(_df[left_column].dtype) # Make sure right_column has same data type as left_column
            
            _df = _df.merge(
                table_df, how=_how, 
                left_on=_left, right_on=_right,
                # suffixes=(f'_{df_table}', f'_{table}')
            ) # join the dfs
            
            _df._tables = tables # Set Current Tables
            
            return _df

        except (KeyError, MySQLError): # the given df may contain multiple tables, if one fails, try the next
            continue
        
    raise TypeError(f'Failed to join {table} With {df._tables}') # No table was suitable for the join params, raise exception


# Queries
DataFrame.join_table = __join_table
DataFrame.table_query = Queries.table_query
