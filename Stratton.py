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
bestChromosome = Chromosome(_genome=[5, 5, 'adadelta', 0.01, 88, 'softsign', 0.04576833916314136, 79, 'elu', 0.06757651750820325, 72, 'softmax', 0.0976546003775951, 66, 'relu', 0.15397405452066762, 87, 'sigmoid', 0.09760566738314312, 1, 'hard_sigmoid'], _maxHL=5)

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

'''
    Saves a model in the directory specified by user.

    Args:   DNN _dnn = model you want to save
'''
def save_model (_dnn):
    directory = input('\nEnter path to the directory to save model: ')
    
    try:
        _dnn.save(directory)
    except Exception as e:
        print(str(e))
        print('\n\nFailed to save model!\n\n')

'''
    Loads a model in the directory specified by user.

    Returns:DNN = loaded DNN
'''
def load_model ():
    directory = input('\nEnter path to the directory to load model from: ')

    dnn = None
    try:
        dnn = DNN(_saveDirectory=directory)
    except Exception as e:
        print(str(e))
        print('\n\nFailed to load model!\n\n')

    return dnn

#TODO: make this give a different Chromosome for each symbol.
'''
    Returns the best Chromosome for any symbol.

    Returns:Chromosome = best Chromosome for a symbol
'''
def _get_best_chromosome(_symbol):
    return bestChromosome

'''
    Trains a model with user specified information.

    Args:   DNN _dnn = dnn to train. If None type, blank model will be created

    Returns:DNN = trained model
'''
def train_model (_dnn):
    symbol = input('\nEnter the stock symbol train model with: ')
    timeSeries = input('Enter the time series: ')
    timeInterval = input('Enter the time interval: ')
    if timeInterval == '':
        timeInterval = None
    
    testPercentage = float(input('Enter fraction of data to test with: '))

    epochs = input('Enter epochs to train for (8): ')
    if epochs == '':
        epochs = 8
    epochs = int(epochs)
    
    batchSize = input('Enter batch size (10): ')
    if batchSize == '':
        batchSize = 10
    batchSize = int(batchSize)

    try:
        return _train_model(symbol, timeSeries, timeInterval, testPercentage, \
                        _dnn, epochs, batchSize)
    except FileNotFoundError as e:
        print(str(e), '\n\n')
        print('\n\nData file not found!\n\n')
        return _dnn
    except Exception as e:
        print(str(e), '\n\n')
        print('\n\nError training model!\n\n')
        return _dnn

'''
    Helper function that actually does the trainined for train_model().

    Args:   _symbol = stock symbol to use
            _timeSeries = time series
            _timeInterval = time interval
            _testPercentage = percentage of data to use for testing (0, 1)
            _dnn = model to train
            _epochs = epochs to train model for
            _batchSize = batch size to train with

    Returns:DNN = trained DNN
'''
def _train_model (_symbol, _timeSeries, _timeInterval, \
                    _testPercentage, _dnn=None, _epochs=8, _batchSize=10):

    trainInputs, trainOutputs, testInputs, testOutputs = load_split_data( \
            _symbol, _timeSeries, _timeInterval, _testPercentage)

    if _dnn == None:
        _dnn = DNN(_chromosome=_get_best_chromosome(_symbol))
        _dnn.compile(bestChromosome.optimizer(), 'mean_squared_error')

    _dnn.train(trainInputs, trainOutputs, _epochs, _batchSize)
    
    print('trained model directional accuracy:', _dnn.evaluate_directional_accuracy(testInputs, testOutputs))
    return _dnn

#TODO add trading bot stuff in here
'''
    Simulates trading with a DNN. Trading settings are supplied by user input.
'''
def trade (_dnn):

    symbol = input('\nEnter the stock symbol train model with: ')
    timeSeries = input('Enter the time series: ')
    timeInterval = input('Enter the time interval: ')
    if timeInterval == '':
        timeInterval = None
    
    testPercentage = float(input('Enter fraction of data to trade with: '))

    try:
        _trade(symbol, timeSeries, timeInterval, testPercentage, _dnn)
    except FileNotFoundError as e:
        print(str(e), '\n\n')
        print('\n\nData file not found!\n\n')
    except Exception as e:
        print(str(e), '\n\n')
        print('\n\nError trading!\n\n')

'''

    Helper function for trade() to simulate trading.

    Args:   _symbol = stock symbol to use
            _timeSeries = time series
            _timeInterval = time interval
            _testPercentage = percentage of data to use for testing (0, 1)
            _dnn = model to train
'''
def _trade (_symbol, _timeSeries, _timeInterval, _testPercentage, _dnn):
    trainInputs, trainOutputs, testInputs, testOutputs = load_split_data( \
            _symbol, _timeSeries, _timeInterval, _testPercentage)

    # TODO add trade bot functions. Print directional accuracy for now
    # get predictions for trading part of split data
    results = _dnn.evaluate_directional_accuracy(testInputs, testOutputs)
    print('results:', results)
    return results

'''
    Prints the main menu of optinos.

    Returns int = user choice
'''
def print_main_menu ():
    print('\n\n1 == Update Symbol Data')
    print('2 == Load Model')
    print('3 == Save Model')
    print('4 == Train New/Current Model')
    print('5 == Trade with Current Model')
    print('6 == Clear Current Model')
    print('0 == Quit')

    choice = input('\nEnter the number for the option you want: ')

    try:
        choice = int(choice)
    except Exception as e:
        choice = choice

    return choice

'''
    Main runtime loop for Stratton trading system.
'''
if __name__ == '__main__':

    print('Welcome to the Stratton simluated stock trading system.')

    currentDNN = None
    choice = -1
    while choice != 0:
        choice = print_main_menu()

        if choice == 1:
            update_data()
        
        elif choice == 2:
            currentDNN = load_model()

        elif choice == 3:
            if currentDNN == None:
                print('\n\nNo current model to save!\n\n')
            else:
                save_model(currentDNN)

        elif choice == 4:
            currentDNN = train_model(currentDNN)

        elif choice == 5:
            if currentDNN == None:
                print('\n\nCannot trade with no current model!\n\n')
            else:
                trade(currentDNN)

        elif choice == 6:
            currentDNN = None

        elif choice == 0:
            print('Quitting')

        else:
            print('\n\n', choice, 'is not a valid choice.\n\n')

