APIKEY = 'SM7GE35DSMNWSBPD' # hard code this for now

import urllib.request
import sys
from Paths import create_data_dir_path
import os
import os.path
import csv

def _create_data_dir_path ():
    if 'Windows' in platform.platform():
        return '..\data'
    else:
        return '../data'

def _create_url (_symbol, _timeSeries, _timeInterval=None, _apiKey = APIKEY):
    url = ''

    if _timeSeries == 'TIME_SERIES_INTRADAY' && _timeInterval != None:
        url = 'https://www.alphavantage.co/query?function=' + _timeSeries + '&symbol=' \
                                 + _symbol + '&interval=' + _timeInterval + '&outputsize=full' + \
                                 '&apikey=' + _apiKey + '&datatype=csv'
    
    else if _timeSeries != 'TIME_SERIES_INTRADAY' && _timeInterval == None:
        url = 'https://www.alphavantage.co/query?function=' + _timeSeries + '&symbol=' \
                                + _symbol + '&outputsize=full' + '&apikey=' + _apiKey + '&datatype=csv'

    else:
        raise ValueError ('_timeSeries and _timeInterval are not compatible')

    return url

def _download_symbol_data (_dlDirectory, _filename, _symbol, _timeSeries, _timeInterval=None, _apiKey=APIKEY):
    
    # save current working directory
    oldPath = os.getcwd()
    
    # check if _dlDirectory exists, if not, create it
    if not os.path.exists(_dlDirectory):
        os.mkdir(_dlDirectory)
    os.chdir(_dlDirectory)


    # download data
    url = _create_url(_symbol, _timeSeries, _timeInterval, _apiKey)
    print('downloading', url)
    urllib.request.urlretrieve(url, _filename)

    # restore current working directory
    os.chdir(oldPath)

def update_symbol_data (

        dataDir = create_data_dir_path()
