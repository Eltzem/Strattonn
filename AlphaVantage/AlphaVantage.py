import sys
import urllib.request
import os
import os.path
import csv

'''
Creates the filename to save a csv download as.
'''

def createQuoteFilename (_symbol, _timeSeries, _timeInterval=None):
    if _timeInterval == None:
        return _symbol + '_' + _timeSeries + '.csv'
    else:
        return _symbol + '_' + _timeSeries + '_' + _timeInterval + '.csv'


'''
Get stock quotes for one stock symbol. Simple interface with the AlphaVantage API.

_directory: path to directory to place download
_symbol: String of the stock symbol
_timeSeries: time series for AlphaVantage (ex: TIME_SERIES_INTRADAY, TIME_SERIES_DAILY)
_apiKey: AlphaVantage API key
_timeInteveral: time interval if using TIME_SERIES_INTRADAY (ex: 1min, 5min, 10min)
'''
def getQuotesCSV (_directory, _symbol, _timeSeries, _apiKey, _timeInterval=None):
    
    url = ''
    filename = ''

    if _timeInterval == None:
        url = 'https://www.alphavantage.co/query?function=' + _timeSeries + '&symbol=' \
                + _symbol + '&outputsize=full' + '&apikey=' + _apiKey + '&datatype=csv'

    else:
        url = 'https://www.alphavantage.co/query?function=' + _timeSeries + '&symbol=' \
                + _symbol + '&interval=' + _timeInterval + '&outputsize=full' + '&apikey=' + _apiKey + '&datatype=csv' 

    filename = createQuoteFilename(_symbol, _timeSeries, _timeInterval)

    # save current directory
    oldPath = os.getcwd()

    if not os.path.exists(_directory):
        os.mkdir(_directory)
    os.chdir(_directory)    
    
    print(url)
    #print(filename)
    #print()

    urllib.request.urlretrieve(url, filename)

    # restore previous directory
    os.chdir(oldPath)


'''
Gets quotes for a list of stock symbols. File containing stock symbols should have a new symbol
on each line.

_symbolFilePath: path to file containing stock symbols
_directory: path to directory to place downloads
_timeSeries: time series for AlphaVantage (ex: TIME_SERIES_INTRADAY, TIME_SERIES_DAILY)
_apiKey: AlphaVantage API key
_timeInteveral: time interval if using TIME_SERIES_INTRADAY (ex: 1min, 5min, 10min)
'''
def getQuotesCSVBatch (_symbolFilePath, _directory, _timeSeries, _apiKey, _timeInterval=None):

    with open(_symbolFilePath) as symbolFile:
        for line in symbolFile:
            getQuotesCSV(_directory, line[:-1], _timeSeries, _apiKey, _timeInterval)

'''
TODO: create a function (s) that get new quote data and append that to the old data
def updateQuote (_fileToUpdate, apiKey):
'''

'''
Run this file to get a batch of stock quotes. File containing stock symbols should have a new symbol
on each line.

Command Line Args:
    1 - path to file containing stock symbol list
    2 - directory path to put csv downloads in
    3 - time series to use (ex: TIME_SERIES_INTRADAY, TIME_SERIES_DAILY, TIME_SERIES_WEEKLY, TIME_SERIES_MONTHLY)
    4 - Alpha Vantage API key
    5 (optional) - time interval if using TIME_SERIES_INTRADAY (ex: 1min, 5min, 15min, 30min, 60min)
'''

if __name__ == '__main__':

    # intraday time series not specified
    if len(sys.argv) <= 5:
        getQuotesCSVBatch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        getQuotesCSVBatch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
