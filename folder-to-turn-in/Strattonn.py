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

import warnings


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

'''
    Returns the best Chromosome for any symbol.

    Returns:Chromosome = best Chromosome for a symbol
'''
def _get_best_chromosome(_symbol, _timeSeries):
    bestChromosome = [5, 5, 'adadelta', 0.01, 88, 'softsign', 0.04576833916314136, 79, 'elu', 0.06757651750820325, 72, 'softmax', 0.0976546003775951, 6, 'relu', 0.15397405452066762, 87, 'sigmoid', 0.09760566738314312, 1, 'hard_sigmoid']

    # set bestChromosome based on which symbol and time series is used

    if _symbol == 'VTI':
        bestChromosome = [5, 5, 'rmsprop', 0.01, 93, 'softsign', 0.15362441542938934, 75, 'softmax', 0.1565223157066145, 55, 'tanh', 0.1393400382909604, 70, 'sigmoid', 0.026028148633672, 1, 'elu']
        if not _timeSeries == 'TIME_SERIES_INTRADAY':
            bestChromosome = [5, 5, 'nadam', 0.01, 78, 'softsign', 0.034350732448751246, 43, 'softsign', 0.18098339839165556, 35, 'sigmoid', 0.023275447336313128, 81, 'softsign', 0.05317601402309749, 54, 'sigmoid', 0.07678868150480041, 1, 'linear']
            
    elif _symbol == 'INX':
        bestChromosome = [5, 5, 'adadelta', 0.01, 88, 'softsign', 0.04576833916314136, 79, 'elu', 0.06757651750820325, 72, 'softmax', 0.0976546003775951, 6, 'relu', 0.15397405452066762, 87, 'sigmoid', 0.09760566738314312, 1, 'hard_sigmoid'] 
        if not _timeSeries == 'TIME_SERIES_INTRADAY':
            bestChromosome = [5, 5, 'rmsprop', 0.01, 22, 'softmax', 0.17782560849448908, 48, 'selu', 0.15507248730671644, 9, 'sigmoid', 0.12337472952083328, 59, 'tanh', 0.0675181009874043, 8, 'hard_sigmoid', 0.06404924191773365, 1, 'softsign']
    
    elif _symbol == 'AAPL':
        bestChromosome = [5, 5, 'adagrad', 0.01, 60, 'softsign', 0.17824595166912402, 94, 'selu', 0.015902688785115315, 47, 'softmax', 0.13297658472589025, 98, 'selu', 0.11169883639392125, 88, 'selu', 0.006811302164357991, 1, 'elu']
        if not _timeSeries == 'TIME_SERIES_INTRADAY':
            bestChromosome = [5, 5, 'adagrad', 0.01, 60, 'softsign', 0.17824595166912402, 94, 'selu', 0.015902688785115315, 47, 'softmax', 0.13297658472589025, 98, 'selu', 0.11169883639392125, 88, 'selu', 0.006811302164357991, 1, 'elu']
    
    elif _symbol == 'AMD':
        bestChromosome = [5, 5, 'nadam', 0.01, 84, 'softsign', 0.18136838939868302, 51, 'softsign', 0.16795021897623255, 5, 'linear', 0.13899004035932758, 74, 'selu', 0.026186657211977528, 1, 'elu'] 
        if not _timeSeries == 'TIME_SERIES_INTRADAY':
            bestChromosome = bestChromosome # no search done for this one

    elif _symbol == 'XOM':
        bestChromosome = [5, 5, 'nadam', 0.01, 4, 'relu', 0.03677919272467345, 98, 'softsign', 0.013660965955586591, 11, 'softplus', 0.19106350430874144, 25, 'hard_sigmoid', 0.055009139864329384, 20, 'elu', 0.1744443475777589, 1, 'elu']
        if not _timeSeries == 'TIME_SERIES_INTRADAY':
            bestChromosome = [5, 5, 'adam', 0.01, 33, 'relu', 0.04787728882744513, 59, 'softmax', 0.09619899765104607, 25, 'elu', 0.01324936861316961, 88, 'relu', 0.19084488481047215, 3, 'softmax', 0.1268256558577213, 1, 'relu']

    # rectify _maxHL in Chromosomes to match
    #print('MAKING CHROMOSOME')
    sizes, dropouts, activations = Chromosome(_genome=bestChromosome).hidden_layers()
    #print('MADE CHROMOSOME')
    maxHL = len(sizes)
    #print('GOT SIZES')

    return Chromosome(_genome=bestChromosome, _maxHL=maxHL)

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
    
    try:
        testPercentage = float(input('Enter fraction of data to test with: '))
    except Exception as e:
        print("enter a valid number between 0 and 1\n\n\n")
        print("\n\nError training model!\n\n")
        return _dnn

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
        _dnn = DNN(_chromosome=_get_best_chromosome(_symbol, _timeSeries))
        _dnn.compile(_dnn.get_chromosome().optimizer(), 'mean_squared_error')

    _dnn.train(trainInputs, trainOutputs, _epochs, _batchSize)
    
    print('\ntrained model directional accuracy:', _dnn.evaluate_directional_accuracy(testInputs, testOutputs))
    return _dnn

#TODO add trading bot stuff in here
'''
    Simulates trading with a DNN. Trading settings are supplied by user input.
'''
def trade (_dnn):

    symbol = input('\nEnter the stock symbol trade with: ')
    timeSeries = input('Enter the time series: ')
    timeInterval = input('Enter the time interval: ')
    if timeInterval == '':
        timeInterval = None
    
    try:
        testPercentage = float(input('Enter fraction of data to trade with: '))
    except Exception as e:
        print("enter a valid number between 0 and 1\n\n\n")
        print("\n\nError trading!\n\n")
        return

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
    print('\nmodel could trade with a directional accuracy of:', results)
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
    # turn off annoying warning messages that don't apply
    warnings.filterwarnings("ignore")

    print('\n\nWelcome to the Stratton simluated stock trading system.')

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
            if not currentDNN == None:
                currentDNN.close()
            currentDNN = None

        elif choice == 0:
            print('Quitting')

            if not currentDNN == None:
                currentDNN.close()

        else:
            print('\n\n', choice, 'is not a valid choice.\n\n')

