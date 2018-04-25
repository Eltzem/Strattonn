''' This file is here to handle creation of paths for files. It can help us manage operating
    system path differences.
'''

import platform

'''
    Returns relative path to the data directory from the program's file location.

    Returns:string = relative path to data directory
'''
#tested
def get_data_dir_path ():
    if 'Windows' in platform.platform():
        return 'data'
    else:
        return 'data'

'''
    Returns the proper directory seperator in a file path for the operating system being used.

    Returns:string = operating system path slash
'''
#tested
def get_path_slash ():
    if 'Windows' in platform.platform():
        return '\\'
    else:
        return '/'


'''
    Gets the relative path to the folder holding formatted data files for a time series.

    Returns:string = path to time series data folder
'''
def get_time_series_data_path (_timeSeries, _timeInterval=None):
    # extract subfolder name and add to dataDir
        # if intraday, use time interval (1min, 5min...)
        # if interday, use time series (daily, monthly...)
    if _timeSeries == 'TIME_SERIES_INTRADAY' and _timeInterval != None:
        return get_data_dir_path() + get_path_slash() + _timeInterval
            
    elif _timeSeries != 'TIME_SERIES_INTRADAY' and _timeInterval == None:    
        return get_data_dir_path() + get_path_slash() + _timeSeries[12:].lower()
    else:
        raise ValueError ('_timeSeries and _timeInterval are not compatible')


'''
    Gets the relative path to the formatted data files for a stock symbol.

    returns:string = path to symbol formatted data file
'''
def get_symbol_data_path (_symbol, _timeSeries, _timeInterval=None):
    # extract subfolder name and add to dataDir
        # if intraday, use time interval (1min, 5min...)
        # if interday, use time series (daily, monthly...)
    if _timeSeries == 'TIME_SERIES_INTRADAY' and _timeInterval != None:
        #print(1)
        return get_data_dir_path() + get_path_slash() + _timeInterval + get_path_slash() + _symbol + \
            '.csv'
            
    elif _timeSeries != 'TIME_SERIES_INTRADAY' and _timeInterval == None:    
        #print(2)
        return get_data_dir_path() + get_path_slash() + _timeSeries[12:].lower() + get_path_slash() + _symbol + \
            '.csv'
    else:
        raise ValueError ('_timeSeries and _timeInterval are not compatible')


'''
    Sames as get_symbol_data_path(), but removes .csv from the end.

    Returns:string = path to symbol formatted data file minus .csv at the end
'''
def get_symbol_data (_symbol, _timeSeries, _timeInterval=None):
    # extract subfolder name and add to dataDir
        # if intraday, use time interval (1min, 5min...)
        # if interday, use time series (daily, monthly...)
    if _timeSeries == 'TIME_SERIES_INTRADAY' and _timeInterval != None:
        return get_data_dir_path() + get_path_slash() + _timeInterval + get_path_slash() + _symbol
            
    elif _timeSeries != 'TIME_SERIES_INTRADAY' and _timeInterval == None:
        return get_data_dir_path() + get_path_slash() + _timeSeries[12:].lower() + get_path_slash() + _symbol
    else:
        raise ValueError ('_timeSeries and _timeInterval are not compatible')

'''
	Returns the data  file path for the training data of a symbol if they are
	split.
'''
def get_symbol_train_data_path (_symbol, _timeSeries, _timeInterval):
    return get_symbol_data (_symbol, _timeSeries, _timeInterval) + '-TRAINSPLIT' \
            + '.csv'

'''
	Returns the data file path for the testing data of a symbol if they are
	split.
'''
def get_symbol_test_data_path (_symbol, _timeSeries, _timeInterval):
    return get_symbol_data (_symbol, _timeSeries, _timeInterval) + '-TESTSPLIT' \
            + '.csv'

