## 13/12/2023 - Daniel

## Build for pypi
```shell
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
```

## Push to the pypi test repository 
```shell
python3 -m twine upload --repository testpypi dist/*
```

## Push to the pypi main repository 
```shell
python3 -m twine upload --repository pypi dist/*
```


# banner.connection:
    ## Connection(Object):
        - ABS class

    ## RelationalConnection(Connection):
        - ABS class

    ## Storage(Connection):
        - ABS class

    ## PrintableConnection(Connection):
        - ABS class

    ## MySqlConnection(RelationalConnection, PrintableConnection)(host, user, passwd, db, ssl_key, ssl_cert, name):
        - Create Connection object compatible with banner.queries  
        - **raises MySQLError for bad connection**

    ## PostgresSqlConnection(RelationalConnection, PrintableConnection)(host, user, port=5432, passwd=None, db=None, ssl_key=None, ssl_cert=None, charset='utf8', name=None):
        - Create Connection object compatible with banner.queries  
        - **raises MySQLError for bad connection**
        
    ## RedisConnection(Storage, PrintableConnection)(host, port, passwd, db, ssl_key, ssl_cert, name, ttl):
        - Create CacheConnection object compatible with banner.queries  

# banner.queries.Queries:
    ## CONNECTIONS(conns: Dict[str, Connection] = {}) -> :
        - Getter/Setter for known(default) Connections dict

    ## CACHE(con: CacheConnection = None):
        - Getter/Setter for known(default) CacheConnection

    ## simple_query(query: str, w2p_parse: bool = True, connection: Union[Connection, str] = None, cache: Storage = None, ttl: int = None) -> pd.DataFrame:
        - run a simple string query for Connection
        - connection=None try to get first known connection, **raise KeyError if None found**
        - Cache the result if cache_connection or Queries.CACHE is set (ttl if provided otherwise use CACHE.ttl)
        - Cache=False will not cache the result even if Queries.CACHE is set
        - w2p_parse=True - should parse query according to w2p syntax
    
    ## describe_table(table: str, connection: Union[RelationalConnection, str] = None) -> pd.DataFrame:
        - Describes a table in connection
        - Raises OperationalError and KeyError(Failed to find a connection for given key) 

    ## describe(connection: Union[RelationalConnection, str] = None) -> pd.DataFrame:
        - Describe Table names in connection
        - Raises OperationalError and KeyError(Failed to find a connection for given key)

    ## table_query(table: str, columns: Union[list, str] = '*', condition: str = 'TRUE', connection=None, cache_connection=None, ttl=None, raw=False) -> pd.DataFrame:
        - Queries a given connection for 'SELECT {columns} FROM {table} WHERE {condition}'
        - Accepts both column values and labels
        - raw=True - column names as in db
        - Queries a given Connection(ip)/str of a known connection (or first known) return result as DataFrame
        - Cache the result if cache_connection or Queries.CACHE is set (ttl if provided otherwise use CACHE.ttl)
        - Cache=False will not cache the result even if Queries.CACHE is set
        - Raises OperationalError and KeyError(Failed to find a connection for given key) 

    ## neware_cache_query(keys: Iterable, condition: str = 'TRUE', connection: Union[MySqlConnection, str] = None, cache: Storage = None, ttl: int = None) -> pd.DataFrame:
        - simplified query to retrieve aggregate cache data by condition
        - condition is a valid where clause for given connection type
        - requires keys in the form Iterable(Tuple(ip, device, unit, channel, test)), ex: [(241, 240222, 6, 11, 2818575226)]
        - Cache the result if cache_connection or Queries.CACHE is set (ttl if provided otherwise use CACHE.ttl)
        - Cache=False will not cache the result even if Queries.CACHE is set

    ## neware_query(device: int, unit: int, channel: int, test: int, connection: Union[Connection, str] = None, cache_connection=None, ttl=None, raw=False, dqdv=False, condition: str = '1', temperature: bool = True, cache_data: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        - query Connection for device, unit, channel, test 
        - connection=None try to get first known connection, **raise KeyError if None found**
        - temperature=True - fetch temperature data
        - raw=False - compute temperature, voltage, current aswell as grouping by auxchl_id
        - dqdv=True -> banner.neware.calc_dq_dv 
        - Cache the result if cache_connection or Queries.CACHE is set (ttl if provided otherwise use CACHE.ttl)
        - Cache=False will not cache the result even if Queries.CACHE is set
        - **raises Type err if no data exists**

    ## neware_tests_query(table: str, experiments: Union[list, Number, str] = [], templates: Union[list, Number, str] = [], tests: Union[list, Number, str] = [], cells: Union[list,Number, str] = [], condition: str = 'cycle < 2', raw=False, dqdv=False, temperature: bool = True, connection: Union[Connection, str] = None, cache_connection=None, ttl=None):
        - Multi Process Queries.neware_query (number of processes = number of distinct connections found for input)
        - Queries all available tests for given table AND experiments AND templates AND tests AND cells
        - Union[list, Number, str] - single/list of numbers or a valid query
        - temperature=True - fetch temperature data
        - raw=False - compute temperature, voltage, current aswell as grouping by auxchl_id
        - dqdv=True -> banner.neware.calc_dq_dv 
        - Cache the result if cache_connection or Queries.CACHE is set (ttl if provided otherwise use CACHE.ttl)
        - Cache=False will not cache the result even if Queries.CACHE is set
        - **raises Type err if no data exists**

# banner.neware:
    ## NEWARE_STEPS:
        - Step number : Step Name Dictionary 

    ## calculate_neware_columns(data: pd.DataFrame):
        - calculate neware columns for a valid neware DataFrame

    ## calculate_dq_dv(data: pd.DataFrame, raw=False):
        - Calculate DQ/DV for a valid neware df
        - raw=False: remove outliers

    ## merge_cache(data: pd.DataFrame, cache_data: pd.DataFrame):
        - Given data(neware df), cache_data(neware_cache df), tries to merge cache_data into data  
        - ** Raises TypeError and Index Error**

# banner.utils.web2py:
    ## JOINS:
        - Default Joins dictionary
        - Used when calling DataFrame.join_table without specifing how to join

    ## COLUMN_TO_LABEL: 
        - Column : Label Dictionary
    
    ## LABEL_TO_COLUMN: 
        - Label : Column Dictionary

# banner.pandas_decorator:
    ## Added functionality onto Pandas.DataFrame object

    ## DataFrame.table_query
        - banner.queries.Queries.table_query

    ## DataFrame.calculate_neware_columns 
        - banner.neware.calculate_neware_columns

    ## DataFrame.calculate_dq_dv 
        - banner.neware.calculate_dq_dv

    ## join_table(table: str, columns: Union[list, str] = '*', condition: str = 'TRUE', left: Union[str, list, None] = None, right: Union[str, list, None] = None, how: Union[str, None] = None, connection: Union[RelationalConnection, str] = None,  raw: bool = False, cache: Storage=None, ttl: Union[bool, None] = None) -> pd.DataFrame:
        - Given a table, Join its relevant Data with the current table_query DataFrame!
        - table: any table under the available Connection
        - columns: select specific columns from the table, default=All
        - condition: additional filtering condition on merged data
        - left: columns used to merge left DataFrame, default is picked from banner.utils.web2py.JOINS
        - right: columns used to merge right DataFrame, default is picked from banner.utils.web2py.JOINS
        - how: how to merge left and right, default is picked from banner.utils.web2py.JOINS
        - connection=None try to get first known connection, **raise KeyError if None found**
        - **raise TypeError If failed to join**