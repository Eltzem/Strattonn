from AlphaVantage import update_symbol_data

from Chromosome import Chromosome
from DNN import DNN

from Paths import get_data_dir_path
from Paths import get_path_slash
from Paths import get_time_series_data_path
from Paths import get_symbol_data_path
from Paths import get_symbol_data

import os
import os.path

import csv

# from TradeBot import TradeBot

'''
    Updates data for a  stock symbol the user specifies.
'''
def update_data ():

    symbol = input('\nEnter the stock symbol to update data for: ')
    timeSeries = input('Enter the time series: ')
    timeInterval = input('Enter the time interval: ')

    try:
        update_symbol_data(symbol, timeSeries, timeInterval)
        updateFailed = False
    except Exception as e:
        print(str(e))
        print('\n\nData update failed!\n\n')

'''
    Splits a data file into training and testing data files. The last few
    percent of the data file will be made into testing data to conduct
    simulated trading with.
'''
def _split_data (_symbol, _timeSeries, _timeInterval):
    

# def _train_model (_symbol, _timeSeries, _timeInterval, _testPercentage):

# def _trade (_symbol, _timeSeries, _timeInterval, _testPercentage):

# def trade ():
    # get user input
    # check if data file exists
        # ask to download if doesn't
    # _split_data
    # _train_model
    # _trade
    # print results
