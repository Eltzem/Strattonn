from AlphaVantage import update_symbol_data

from Chromosome import Chromosome
from DNN import DNN

from Paths import get_data_dir_path
from Paths import get_path_slash
from Paths import get_time_series_data_path
from Paths import get_symbol_data_path
from Paths import get_symbol_data
from Paths import get_symbol_train_data_path
from Paths import get_symbol_test_data_path

from LoadData import load_data
from LoadData import load_split_data

import random

import os
import os.path

import csv

# TODO update with real best Chromosome
bestChromosome = Chromosome(_genome=[5, 5, 'adam', 0.01, 100, 'linear', 0.020142039851822835, 32, 'softmax', 0.11389427288630116, 78, 'selu', 0.19300485138497203, 43, 'softsign', 0.12657293241015408, 60, 'relu', 0.16140356082279383, 1, 'softsign'], _maxHL=5)

# from TradeBot import TradeBot

'''
    Updates data for a  stock symbol the user specifies.
'''
#tested
def update_data ():

    symbol = input('\nEnter the stock symbol to update data for: ')
    timeSeries = input('Enter the time series: ')
    timeInterval = input('Enter the time interval: ')
    if timeInterval == '':
        timeInterval = None

    try:
        update_symbol_data(symbol, timeSeries, timeInterval)
        updateFailed = False
    except Exception as e:
        print(str(e))
        print('\n\nData update failed!\n\n')


def _train_model (_symbol, _timeSeries, _timeInterval, \
                    _testPercentage, _dnn=None, _epochs=8, _batchSize=10):

    trainInputs, trainOutputs, testInputs, testOutputs = load_split_data( \
            _symbol, _timeSeries, _timeInterval, _testPercentage)

    if _dnn == None:
        _dnn = DNN(_chromosome=bestChromosome)
        _dnn.compile(bestChromosome.optimizer(), 'mean_squared_error')

    _dnn.train(trainInputs, trainOutputs, _epochs, _batchSize)

    return _dnn

def _trade (_symbol, _timeSeries, _timeInterval, _testPercentage, _dnn):
    trainInputs, trainOutputs, testInputs, testOutputs = load_split_data( \
            _symbol, _timeSeries, _timeInterval, _testPercentage)

    # TODO add trade bot functions
    # get predictions for trading part of split data
    return _dnn.evaluate_directional_accuracy(testInputs, testOutputs)

# def trade ():
    # get user input
    # check if data file exists
        # ask to download if doesn't
    # load model from disk?
    # _train_model
    # _trade
    # print results
    # save model?
