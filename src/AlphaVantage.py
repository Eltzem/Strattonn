APIKEY = 'SM7GE35DSMNWSBPD' # hard code this for now

import urllib.request
import sys
from Paths import create_data_dir_path
from Paths import get_path_slash
import os
import os.path
import csv

# tested
def _create_url (_symbol, _timeSeries, _timeInterval=None, _apiKey = APIKEY):
    url = ''

    if _timeSeries == 'TIME_SERIES_INTRADAY' and _timeInterval != None:
        url = 'https://www.alphavantage.co/query?function=' + _timeSeries + '&symbol=' \
                                 + _symbol + '&interval=' + _timeInterval + '&outputsize=full' + \
                                 '&apikey=' + _apiKey + '&datatype=csv'
    
    elif _timeSeries != 'TIME_SERIES_INTRADAY' and _timeInterval == None:
        url = 'https://www.alphavantage.co/query?function=' + _timeSeries + '&symbol=' \
                                + _symbol + '&outputsize=full' + '&apikey=' + _apiKey + '&datatype=csv'

    else:
        raise ValueError ('_timeSeries and _timeInterval are not compatible')

    return url

# tested
def _format_csv (_filepath):
    if not os.path.exists(_filepath):
        raise Exception ('Filepath does not exist:', _filepath)

    filepathNew = _filepath + '.tmp'

    with open(_filepath) as fOld:
        csvOld = csv.reader(fOld)
        
        with open(filepathNew, 'w') as fNew:
            csvNew = csv.writer(fNew)
            
            # skip first line
            next(csvOld)

            # write header
            csvNew.writerow(['year', 'month', 'day', 'hour', 'minute', 'open', 'close', 'low', \
                                'high', 'volume'])

            # extract data for each row
            for row in csvOld:

                # date
                year = int(row[0][ : 4])

                month = int(row[0][5 : 7])

                day = int(row[0][8 : 10])

                hour = int(row[0][11 : 13])

                minute = int(row[0][14 : 16])

                # trade stats
                openPrice = row[1]
                highPrice = row[2]
                lowPrice = row[3]
                closePrice = row[4]
                volume = row[5]

                # write data
                csvNew.writerow([year, month, day, hour, minute, openPrice, closePrice, lowPrice, \
                                    highPrice, volume])

    os.remove(_filepath)
    os.rename(filepathNew, _filepath)

def _append_data (_existing, _new):
    return

# tested
def _download_symbol_data (_dlDirectory, _filename, _symbol, _timeSeries, _timeInterval=None, _apiKey=APIKEY):
    
    # save current working directory
    oldPath = os.getcwd()
    
    # check if _dlDirectory exists, if not, create it
    if not os.path.exists(_dlDirectory):
        os.mkdir(_dlDirectory)
    os.chdir(_dlDirectory)


    # download data
    try:
        url = _create_url(_symbol, _timeSeries, _timeInterval, _apiKey)
    except ValueError as e:
        print('Data URL creation failed:', str(e))
        raise e
    
    print('downloading', url)
    
    try:
        urllib.request.urlretrieve(url, _filename)
    except Exception as e:
        print('Failed to download data csv:', str(e))
        raise e

    # check if downloaded csv is valid (no API error)
    errorOccurred = False

    with open(_filename) as f:
        csvFile = csv.reader(f)
        next(csvFile) # get first line
        errorLine = next(csvFile)[0]
        # 'Error' in second line, first column of csv, API error occured
        if 'Error' in errorLine:
            print('Failed to download data csv:', errorLine)
            errorOccurred = True

    # delete csv if API error occurred
    if errorOccurred:
        os.remove(_filename)

    # restore current working directory
    os.chdir(oldPath)

def update_symbol_data (_symbol, _timeSeries, _timeInterval=None, apiKey=APIKEY):

        # save current working directory
        oldPath = os.getcwd()

        # go into data directory
        dataDir = create_data_dir_path()
        os.chdir(dataDir)

        # extract subfolder name
            # if intraday, use time interval (1min, 5min...)
            # if interday, use time series (daily, monthly...)
        subfolder = ''
        if _timeSeries == 'TIME_SERIES_INTRADAY' and _timeIntedrval != None:
            subfolder = _timeInterval
        elif _timeSeries != 'TIME_SERIES_INTRADAY' and _timeInterval == None:
            subfolder = _timeSeries[12:].lower()
        else:
            raise ValueError ('_timeSeries and _timeInterval are not compatible')

        
        # check if time series subfolder is there. if not, make it and go in
        if not os.path.exists(subfolder):
            os.mkdir(subfolder)
        os.chdir(subfolder)

        # set filename for new file
        filenameTemp = _symbol + '_temp.csv'

        # download new data
        try:
            _download_symbol_data (os.getcwd(), filenameTemp, _symbol, _timeSeries, \
                    _timeInterval=_timeInterval, _apiKey=APIKEY)
        except Exception as e:
            raise e

        # format csv to our liking
        _format_csv(os.getcwd() + get_path_slash() + filenameTemp)
'''
        # append new data to existing if needed
        if os.path.exists(_symbol + '.csv'):
            

        # else, this file is new. rename it to permanent name
        else:

        # restore current working directory
        os.chdir(oldPath)
'''
