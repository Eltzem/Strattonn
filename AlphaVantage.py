APIKEY = 'SM7GE35DSMNWSBPD' # hard code this for now

#TODO add comments to places

import urllib.request # download data
from Paths import get_data_dir_path
from Paths import get_path_slash
from timestep import timestep # class for a data point
import os # chdir, remove, getcwd
import os.path # exists
import csv # read and write csv
from datetime import datetime # compare dates
import time # sleep to make AlphaVantage happy
import random # create random values to sleep from

''' 
    Creates an AlphaVantage API url for the parameters specified.

    Args:   string _symbol = stock symbol
            string _timeSeries = AlphaVantage time series indicator (ex. TIME_SERIES_INTRADAY)
            string _timeInterval = AlphaVantage time interval indicator. only needed for INTRADAY (ex. 1min)
            string _apiKey = AlphaVantagae api key

    Returns:string url = AlphaVantage url to request
'''
#tested
def _create_url (_symbol, _timeSeries, _timeInterval=None, _apiKey = APIKEY):
    print('_create_url(', _symbol, _timeSeries, _timeInterval, _apiKey, ')')

    url = ''

    if _timeSeries == 'TIME_SERIES_INTRADAY' and _timeInterval != None:
        url = 'https://www.alphavantage.co/query?function=' + _timeSeries + '&symbol=' \
                                 + _symbol + '&interval=' + _timeInterval + '&outputsize=full' + \
                                 '&apikey=' + _apiKey + '&datatype=csv'
    
    elif _timeSeries != 'TIME_SERIES_INTRADAY' and _timeInterval == None:
        url = 'https://www.alphavantage.co/query?function=' + _timeSeries + '&symbol=' \
                                + _symbol + '&outputsize=full' + '&apikey=' + _apiKey + '&datatype=csv'

    else:
        raise ValueError ('AlphaVantage._create_url: _timeSeries and _timeInterval are not compatible')

    return url

'''
    Takes a csv data file line and returns a datetime.datetime object with the date from that timestep.

    Args:   list _line = List directly from a formatted csv data file.

    Returns:datetime.datetime = datetime object for the time of this timestep
'''
#tested
def _csv_line_extract_datetime (_line):
    line = timestep(_line)
    return datetime(year=int(line.year), month=int(line.month), day=int(line.day), hour=int(line.hour), \
                                minute=int(line.minute))

'''
    Takes a csv file directly from AlphaVantage and formats it to our specification. Extracts time information and
    rearranges statistics. Stat order is (year, month, day, hour, minute, open, close, low, high, volume).

    Args:   string _filepath: relative or full filepath to the csv file to format
'''
#tested
def _format_csv (_filepath):
    print('_format_csv(', _filepath, ')')
    
    # check if path exists
    if not os.path.exists(_filepath):
        raise Exception ('Filepath does not exist:' + _filepath)

    # path for temporary file while formatting
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

            rows = [] # hold rows for reversal

            # extract data for each row
            for row in csvOld:
                
                # date extraction
                date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                
                # add row data to dictionary for easy access
                rows.append({'year':date.year, 'month':date.month, 'day':date.day, 'hour':date.hour, \
                                'minute':date.minute, 'openPrice':row[1], 'closePrice':row[4], \
                                'lowPrice':row[3], 'highPrice':row[2], 'volume':row[5]})
            
            # write rows in reverse order
            for i in range(len(rows) - 1, -1, -1):
                # write data in particular order
                csvNew.writerow([ rows[i]['year'], rows[i]['month'], rows[i]['day'], \
                                    rows[i]['hour'], rows[i]['minute'], rows[i]['openPrice'], \
                                    rows[i]['closePrice'], rows[i]['lowPrice'], rows[i]['highPrice'], \
                                    rows[i]['volume'] ])

    # replace unformatted file with formatted file
    os.remove(_filepath)
    os.rename(filepathNew, _filepath)


'''
    Adds new formatted timestep information to an existing csv data file. Only adds lines to the existing file
    that are new. Both csv files must be formatted. 

    Args:   string _filepathSource = relative or full path to the csv containing new data
            string _filepathTarget = relative or full path to the existing csv data file
'''
#tested
def _append_data (_filepathSource, _filepathTarget):
    print('_append_data(', _filepathSource, _filepathTarget, ')')

    fileTarget = open(_filepathTarget, 'r')
    fileSource = open(_filepathSource, 'r')

    csvTarget = csv.reader(fileTarget, delimiter=',') # just need to read lines in memory for now
    csvSource = csv.reader(fileSource, delimiter=',')

    # skip first line in each (header)
    next(csvTarget)
    next(csvSource)

    # extract date from most recent (last) line in target csv
    targetLast = None
    for line in csvTarget:
        targetLast = line
    targetLastDate = _csv_line_extract_datetime(targetLast)

    # re-open target for appending
    fileTarget.close()
    fileTarget = open(_filepathTarget, 'a')

    csvTarget = csv.writer(fileTarget) # now we will write new lines to file

    # loop through all lines in source csv
        # if line's date is after last date in target, append line
    for line in csvSource:
        date = _csv_line_extract_datetime(line)

        if date > targetLastDate:
            csvTarget.writerow(line)

    fileTarget.close()
    fileSource.close()

'''
    Sometimes AlphaVantage returns a csv file with an error message. This function opens the downloaded
    file and tells whether the error message is present.

    Args:   string _filepath = relative or full path to the csv file to check
'''
#tested
def _download_error_occurred (_filepath):
    print('_download_error_occurred(', _filepath, ')')

    if not os.path.exists(_filepath):
        print('\nFailed to download data csv: file does not exist\n')
        return False

    # opens csv file
    with open(_filepath) as f:
        csvFile = csv.reader(f)
        next(csvFile) # get first line
        errorLine = next(csvFile)[0]
        # 'Error' in second line, first column of csv, API error occured
        if 'Error' in errorLine:
            print('\nFailed to download data csv:', errorLine, '\n')
            return True

        return False

'''
    Downloads a csv data file from AlphaVantage with the specified arguments. If download fails for any reason
    (API or HTTP), retry a max of 9 more times. Wait until retry starts at 1 second and doubles for each successive failure.

    Args:   string _dlDirectory = relative or full path to the data directory to download the file into
            string _symbol = stock symbol
            string _timeSeries = AlphaVantage time series indicator (ex. TIME_SERIES_INTRADAY)
            string _timeInterval = AlphaVantage time interval indicator. only needed for INTRADAY (ex. 1min)
            string _apiKey = AlphaVantagae api key
'''
# tested
def download_symbol_data (_dlDirectory, _filename, _symbol, _timeSeries, _timeInterval=None, \
                            _apiKey=APIKEY):
    print('download_symbol_data(', _dlDirectory, _filename, _symbol, _timeSeries, _timeInterval, \
                            _apiKey, ')')


    # save current working directory
    oldPath = os.getcwd()
    
    # check if _dlDirectory exists, if not, create it
    if not os.path.exists(_dlDirectory):
        os.mkdir(_dlDirectory)
    os.chdir(_dlDirectory)


    # download data
    try:
        url = _create_url(_symbol, _timeSeries, _timeInterval, _apiKey)
    except Exception as e:
        print('\nData URL creation failed:', str(e), '\n')
        raise e
    
    # download data from AlphaVantage API
        # try multiple times, as sometimes it says the call failed for no reason and returns a bad csv

    maxAPIFails = 10
    APIFails = 0
    APISuccess = False
    requestWaitTime = 1 # seconds to wait between failed requests

    while not APISuccess and APIFails < maxAPIFails:
        print('downloading', url)
        
        try:
            urllib.request.urlretrieve(url, _filename)
            APISuccess = True # API download succeeded
        except Exception as e:
            print('\nFailed to download data csv:', str(e), '\n')
            APISuccess = False

        # API error occurred
        if _download_error_occurred(_filename):
            APISuccess = False

        # what to do if API request failed
        if not APISuccess:
            APIFails += 1

            # delete partial or error files
            if os.path.exists(_filename):
                os.remove(_filename)
            # from format function
            if os.path.exists(_filename + '.tmp'):
                os.remove(_filename + '.tmp')

            time.sleep(requestWaitTime)
            requestWaitTime *= 2 # keep increasing wait time between requests

    # API failure exceeded threshold, abandon it
    if not APISuccess and APIFails >= maxAPIFails:
        raise Exception('API download failure exceeded threshold of', str(maxAPIFails))

    # restore current working directory
    os.chdir(oldPath)

'''
    Downloads new csv stock data from AlphaVantage. If no data exists for the symbol, just downloads and formats a new csv.
    If data for the symbol, append the new data to the existing. Assumes the data directory is formatted consistently.
    An existing data directory and comments below should adequetely describe the format.

    Args:   string _symbol = stock symbol
            string _timeSeries = AlphaVantage time series indicator (ex. TIME_SERIES_INTRADAY)
            string _timeInterval = AlphaVantage time interval indicator. only needed for INTRADAY (ex. 1min)
            string _apiKey = AlphaVantagae api key
'''
#tested
def update_symbol_data (_symbol, _timeSeries, _timeInterval=None, apiKey=APIKEY):
        print('update_symbol_data(', _symbol, _timeSeries, _timeInterval, apiKey, ')')

        print('Updating symbol data for:', _symbol, 'time series:', _timeSeries, 'timeinterval:', \
                _timeInterval)

        # save current working directory
        oldPath = os.getcwd()

        # create data directory we need
        dataDir = get_data_dir_path() + get_path_slash()

        # extract subfolder name and add to dataDir
            # if intraday, use time interval (1min, 5min...)
            # if interday, use time series (daily, monthly...)
        if _timeSeries == 'TIME_SERIES_INTRADAY' and _timeInterval != None:
            dataDir += _timeInterval
        elif _timeSeries != 'TIME_SERIES_INTRADAY' and _timeInterval == None:
            dataDir += _timeSeries[12:].lower()
        else:
            raise ValueError ('_timeSeries and _timeInterval are not compatible')

        
        # check if dataDir is there. if not, make it and go in
        if not os.path.exists(dataDir):
            os.mkdir(dataDir)
        os.chdir(dataDir)

        # set filename for new file
        filenameTemp = _symbol + '_temp.csv'

        # download new data from AlphaVantage API
        try:
            download_symbol_data (os.getcwd(), filenameTemp, _symbol, _timeSeries, \
                    _timeInterval=_timeInterval, _apiKey=APIKEY)
        except Exception as e:
            raise e

        # format csv to our liking
        _format_csv(os.getcwd() + get_path_slash() + filenameTemp)

        filenamePermanent = _symbol + '.csv'

        # append new data to existing if needed
        if os.path.exists(filenamePermanent):
            _append_data(os.getcwd() + get_path_slash() + filenameTemp, \
                            os.getcwd() + get_path_slash() + filenamePermanent)
            os.remove(filenameTemp)

        # else, this file is new. rename it to permanent name
        else:
            os.rename(filenameTemp, filenamePermanent)

        # restore current working directory
        os.chdir(oldPath)