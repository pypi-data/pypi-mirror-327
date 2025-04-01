from functools import reduce
from datetime import timedelta
from scipy.signal import savgol_filter

import pandas as pd
import numpy as np

try:
    from pandas.core.computation.ops import UndefinedVariableError # pandas < 1.5.0
    
except ImportError:
    from pandas.errors import UndefinedVariableError

from banner.utils.const import (
    NW_VOLTAGE, NW_CURRENT, NW_TEMP, NW_AUX_CHANNEL, NW_STEP_RANGE, 
    NW_TIMESTAMP, NW_DATESTAMP, NW_SEQ, 
    NW_CACHE_CYCLE_SEQ, NW_UNIT, NW_CHANNEL, NW_TEST,
    PREV_SUFFIX, OUTLIER_STD_COEFFECIENT, NW_CACHE_DUR, NW_CYCLE
)

from banner.utils.pandas import assert_required_columns, parse_mysql_to_pandas_query

NEWARE_STEPS = {
    1: "CC_Chg",
    2: "CC_DChg",
    3: "CV_Chg",
    4: "Rest",
    5: "Cycle",
    6: "End",
    7: "CCCV_Chg",
    8: "CP_DChg",
    9: "CP_Chg",
    10: "CR_DChg",
    13: "Pause",
    17: "SIM",
    18: "PCCCV_Chg",
    19: "CV_DChg",
    20: "CCCV_DChg",
}

def calculate_neware_columns(df: pd.DataFrame, cache_df: pd.DataFrame = pd.DataFrame()):
    ''' 
        Assures df is sorted by seq_id
        Performs calculate_voltage, calculate_current, calculate_neware_timestamp, calculate_temperature, group_by_auxchl
        cache_df can be used to calculate_neware_timestamp
        Raises KeyError for missing columns
    '''
    assert_required_columns(df, NW_SEQ)
    
    df = df.sort_values(NW_SEQ)
    
    if NW_VOLTAGE in df:
        df[NW_VOLTAGE] = calculate_voltage(df)
    
    if NW_CURRENT in df and NW_STEP_RANGE in df:
        df[NW_CURRENT] = calculate_current(df)
    
    if NW_TIMESTAMP in df:
        result = calculate_neware_timestamp(df, cache_df=cache_df)
        df[NW_TIMESTAMP] = result.values
    
    temp_columns = [column for column in df.columns if column.startswith(NW_TEMP)] # Temperature columns
    
    if temp_columns:
        df[temp_columns] = df[temp_columns].apply(lambda obj: obj / 10)
    
    return df

def group_by_auxchl(df: pd.DataFrame):
    ''' 
        Group by auxchl_id set test_temp to auxchl_num
    '''
    assert_required_columns(df, NW_TEMP, NW_AUX_CHANNEL)

    merge_columns = [column for column in list(df.columns) if column not in [NW_TEMP, NW_AUX_CHANNEL]]
    # TODO perhaps use pivot for faster calculation
    group_as_list = [
        _df.loc[
            :, _df.columns != NW_AUX_CHANNEL
        ].rename(columns={NW_TEMP: f'{NW_TEMP}{name}'})
        for name, _df in df.groupby(NW_AUX_CHANNEL)
    ]

    return reduce(
        lambda left,right: pd.merge(left, right, on=merge_columns, how='left'),
        group_as_list
    )

def calculate_temperature(df: pd.DataFrame):
    ''' 
        Calculate temp from test_temp
    '''
    assert_required_columns(df, NW_TEMP)
    
    return df[NW_TEMP].apply(lambda obj: obj / 10)
    
def calculate_voltage(df: pd.DataFrame):
    ''' 
        Calculate voltage from test_vol
    '''
    assert_required_columns(df, NW_VOLTAGE)

    return df[NW_VOLTAGE].apply(lambda obj: obj / 10000)

def calculate_current(df: pd.DataFrame):
    ''' 
        Calculate current from test_cur
    '''
    assert_required_columns(df, NW_CURRENT, NW_STEP_RANGE)
    
    coeff = df[NW_STEP_RANGE].apply(__current_coeff)
    current = (df[NW_CURRENT] * coeff).round(3)
    
    return current

def __current_coeff(cur_range):
    return 0.00001 * 10**min(4, len(str(abs(cur_range)))) * (0.1 if cur_range < 0 else 1)

def calculate_neware_timestamp(df: pd.DataFrame, cache_df: pd.DataFrame = pd.DataFrame()):
    ''' 
        Calculate timestamp using test_time, seq_id
    '''
    required_columns = [NW_SEQ, NW_TIMESTAMP]

    assert_required_columns(df, *required_columns)

    _df = df[required_columns]
    
    try: #Try to create cached cycle_end_seq to calculate_neware_timestamp
        cache_df = cache_df.sort_values([NW_CACHE_CYCLE_SEQ])
        
        __cached_cycle_end_seq = pd.Series(data=cache_df[NW_CACHE_DUR].values, index=cache_df[NW_CACHE_CYCLE_SEQ].values)
        
    except (TypeError, KeyError):
        __cached_cycle_end_seq = pd.Series()
    
    prev_timestamp, prev_seq_id = NW_TIMESTAMP + PREV_SUFFIX, NW_SEQ + PREV_SUFFIX
    
    # Remove chained_assignment warning
    __chained_assignment = pd.options.mode.chained_assignment
    pd.options.mode.chained_assignment = None

    # Add prev test_time and prev seq_id to _df
    _df[prev_timestamp] = _df[NW_TIMESTAMP].shift(1)
    _df[prev_seq_id] = _df[NW_SEQ].shift(1)
    
    # Restore chained_assignment warning
    pd.options.mode.chained_assignment = __chained_assignment
    
    # prev test_time and seq_id where current test_time = 0 (all step and cycle ends)
    __cycle_end_seq = _df.loc[
        _df[NW_TIMESTAMP] == 0, 
        [prev_seq_id, prev_timestamp]
    ]
    
    # Create cycle_end_seq of given df
    __cycle_end_seq = pd.Series(data=__cycle_end_seq[prev_timestamp].values, index=__cycle_end_seq[prev_seq_id].values)
    
    # Combine them and sum of prev (combine cache_df into df)
    __cycle_end_seq = __cycle_end_seq.combine_first(__cached_cycle_end_seq).dropna().cumsum()
    
    def __calc_timestamp(seq_range, group):
        try:
            _last_step = __cycle_end_seq[__cycle_end_seq.index < seq_range.right].iloc[-1]
            
            group[NW_TIMESTAMP] = group[NW_TIMESTAMP] + _last_step
        except IndexError:
            pass

        return group
        
    CACHE_SEQ_RANGE = [0] + list(__cycle_end_seq.index) + [np.inf]
    
    return df.groupby(
        pd.cut(
            df[NW_SEQ], 
            CACHE_SEQ_RANGE
        ),
        as_index=False
    ).apply(lambda grp: __calc_timestamp(grp.name, grp))[NW_TIMESTAMP]
    
def calculate_dqdv(df: pd.DataFrame, raw: bool = False, window_length: int = 21) -> pd.Series:
    ''' 
        Calculate DQ/DV for a valid neware df
        raw=False: remove outliers
    '''
    required_columns = [NW_VOLTAGE, NW_CURRENT, NW_TIMESTAMP]

    assert_required_columns(df, *required_columns)
    
    _df = df.copy()
    
    _df = df[required_columns]

    dt = _df[NW_TIMESTAMP] - _df[NW_TIMESTAMP].shift(1)
    
    dv = _df[NW_VOLTAGE] - _df[NW_VOLTAGE].shift(1)
    
    current = _df[NW_CURRENT]
        
    dq = current * dt / 1000 / 3600
    
    dqdv = dq / dv

    if not raw:
        dqdv.replace([np.inf, -np.inf], np.nan, inplace=True)
        dqdv[(np.abs(dqdv - dqdv.mean()) > (OUTLIER_STD_COEFFECIENT * dqdv.std()))] = np.nan

        if window_length % 2 == 1 and window_length < len(dqdv):
            # Apply Savitzky-Golay filter
            # window_length must be odd and smaller than data points
            # polyorder must be smaller than window_length
            polyorder = 3
            dqdv.fillna(method='bfill', inplace=True)
            dqdv = pd.Series(savgol_filter(dqdv, window_length=window_length, polyorder=polyorder))
        
    return dqdv

def merge_cache(df: pd.DataFrame, cache_df: pd.DataFrame, columns=None):
    ''' 
        Merge neware dataframe(data)
        With neware cache dataframe(cache_data)
        Raises TypeError, IndexError for bad input
    '''
    assert_required_columns(df, NW_SEQ)
    assert_required_columns(cache_df, NW_CACHE_CYCLE_SEQ)
    
    cache_df = cache_df.sort_values([NW_CACHE_CYCLE_SEQ]) # make sure cache is order(asc)
    
    CACHE_SEQ_RANGE = [0] + list(cache_df[NW_CACHE_CYCLE_SEQ]) + [np.inf] # Buckets for each cycle
    
    columns = cache_df.columns.intersection(set(columns))

    def __merge_cache(group):
        try:
            cache_row = cache_df[cache_df[NW_CACHE_CYCLE_SEQ] == group.name.right].iloc[-1]
           
            return group.assign(**cache_row[columns])
            
        except IndexError:
            return group
    
    df = df.groupby(
        pd.cut(
            df[NW_SEQ], 
            CACHE_SEQ_RANGE
        )
    ).apply(__merge_cache)

    try:
        df[NW_CYCLE] = df[NW_CYCLE].astype(int, errors='ignore')
        
    except (IndexError, KeyError):
        pass
    
    return df

def query_cache(df: pd.DataFrame, query: str):
    ''' 
        Query df and returnes seq_id ranges
    '''
    try:
        df_by_query = df.query(
            parse_mysql_to_pandas_query(query), engine='python'
        )
        
        ranges = [__query_cache_by_group(df, group_by_query) for index, group_by_query in df_by_query.groupby(df_by_query.index.to_series().diff().ne(1).cumsum())]
        
        assert(ranges)

        return f'({" OR ".join(ranges)})' 

    except AssertionError:
        return '0'

    except (UndefinedVariableError, SyntaxError, TypeError, ValueError):
        return query  

def __query_cache_by_group(df: pd.DataFrame, group: pd.DataFrame):
    first_seq_id = 0
    
    if group.iloc[0][NW_CYCLE] > 1: #Is it the first Cycle?
        first_seq_id = df[df[NW_CYCLE] == group.iloc[0][NW_CYCLE] - 1].iloc[0][NW_CACHE_CYCLE_SEQ]
        
    last_seq_id = group.iloc[-1][NW_CACHE_CYCLE_SEQ]
    
    return f'{NW_SEQ} > {first_seq_id} AND {NW_SEQ} <= {last_seq_id}'

def calculate_capacity(df: pd.DataFrame, normalized=False):
    '''Calculate Capacity'''
    '''Assuming timestamp and current are calculated!'''
    assert_required_columns(df, NW_TIMESTAMP, NW_CYCLE, NW_CURRENT, NW_STEP_RANGE)
    
    capacity, diff, prev_cur = 'capacity', 'test_time_diff', 'prev_test_cur'

    _df = df.copy()

    def __calc_capacity(group):
        group[capacity] = group[diff] * group[NW_CURRENT].abs() / 3600000
        group[capacity] = group[capacity].cumsum()
        
        if normalized:
            try:
                group[capacity] = group[capacity] / group[capacity].max()

            except ZeroDivisionError:
                group[capacity] = 0
    
        return group
        
    def _calc_capacity(group):
        group[diff] = group[NW_TIMESTAMP].diff()
        group[diff].iloc[0] = 0
        group[prev_cur] = group[NW_CURRENT].shift(1)

        cur_change = group[
            ((group[NW_CURRENT] > 0) & (group[prev_cur] <= 0)) | ((group[NW_CURRENT] < 0) & (group[prev_cur] >= 0))
        ].index.values
        
        return group.groupby(pd.cut(
            group.index, 
            [0] + list(cur_change) + [np.inf],
            right=False
        )).apply(__calc_capacity)
    
    return _df.groupby(NW_CYCLE).apply(_calc_capacity)[capacity]

def IS_CALCULATED_NEWARE_DF(df: pd.DataFrame):
    try:
        assert_required_columns(df, NW_TIMESTAMP)

        return not (df[NW_TIMESTAMP].diff() < 0).any()
    except KeyError:

        return False

def calculate_neware_datetime(df: pd.DataFrame):
    assert_required_columns(df, NW_TIMESTAMP, NW_DATESTAMP)
    
    milseconds = (df[NW_TIMESTAMP] % 1000).apply(
        lambda value: timedelta(milliseconds=value)
    )
    
    return df[NW_DATESTAMP] + milseconds
    
