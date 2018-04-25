from Paths import get_symbol_data_path
from Paths import get_symbol_data
from Paths import get_path_slash
from Paths import get_symbol_train_data_path
from Paths import get_symbol_test_data_path

from framePrepDnn import framePrepDnn
from PreprocessCsv import PreprocessCsv



import csv

import random
import os

'''
Loads data for training and testing of models.     Splits data so self.testPercentage is used as the percentage of data for testing.

Returns:    4 lists. Each list contains the da    ta described by the name in format: [ [0data0, 0data1,     0data2], [1data0, 1data1, 1data2], ...]
'''


# returns training and testing data for network. Randomizes it.
def load_training_and_testing_data (_testPercentage, _symbol, _timeSeries, _timeInterval=None):
    print('loading training and testing data')

    inputs, outputs = load_data(_symbol, _timeSeries, _timeInterval)

    print('\nsplitting and randomizing data\n')

    # randomize data
    data = list(zip(inputs, outputs))
    random.shuffle(data)
    inputs, outputs = zip(*data)

    # index to split training and testing data on
    indexDivider = int(len(inputs) * _testPercentage)

    # split data
    testInputs = inputs[:indexDivider]
    testOutputs = outputs[:indexDivider]

    trainInputs = inputs[indexDivider:]
    trainOutputs = outputs[indexDivider:]


    #print('trainInputs:', len(trainInputs))
    #print('trainOutputs:', len(trainOutputs))
    #print('testInputs:', len(testInputs))
    #print('testOutputs:', len(testOutputs))

    #print(testInputs[2])
    #print(testOutputs[2])
    #print(trainInputs[2])
    #print(trainOutputs[2])

    return trainInputs, trainOutputs, testInputs, testOutputs
    
    '''
        Creates a calculated data file for a stock symbol data series. Loads the contents of
        that file into inputs and outputs.
    
        Args:   string _symbol = stock symbol
                string _timeSeries = AlphaVantage time series
                string _timeInterval = optional AlphaVantage time interval (1min, 5min...)

        Returns:input and output data. Formatted the same as specified in the comment for
                load_training_and_testing_data()
    '''

def load_data (_symbol, _timeSeries, _timeInterval=None):
    print('\nloading data\n')

    # call PreprocessCsv class to generate data
    print(get_symbol_data_path(_symbol, _timeSeries, _timeInterval))
    
    c = PreprocessCsv(get_symbol_data_path(_symbol, _timeSeries, _timeInterval))

    # get inputs and outputs from that file
    inputs, outputs = \
                framePrepDnn.framePrepDnn(get_symbol_data(_symbol, _timeSeries, _timeInterval))

    #print(inputs)
    #print(outputs)
        
    return inputs, outputs


'''
    Splits a data file into training and testing data files. The last few
    percent of the data file will be made into testing data to conduct
    simulated trading with.
'''
#tested
def split_data (_symbol, _timeSeries, _timeInterval, _testPercentage):
    # open data file containing all time steps
    f = open(get_symbol_data_path(_symbol, _timeSeries, _timeInterval))
    wholeFile = csv.reader(f)

    # extract data lines from csv
    lines = []
    for line in wholeFile:
        lines.append(line)

    f.close()

    # make sure _testPercentage is suffuciently away from 0 and 1
    if _testPercentage < 0.05:
        _testPercentage = 0.05
    elif _testPercentage > 0.95:
        _testPercentage = 0.95

    # calculate training percentage from _testPercentage
    trainPercentage = 1 - _testPercentage

    # seperate data
    dividerIndex = int(len(lines) * trainPercentage)

    testLines = [lines[0]] # add header to test data
    trainLines = lines[:dividerIndex]
    testLines += lines[dividerIndex:]

    # append data to seperate training and testing csv files
    f = open(get_symbol_train_data_path(_symbol, _timeSeries, _timeInterval), 'w')
    trainCSV = csv.writer(f)

    for line in trainLines:
        trainCSV.writerow(line)

    f.close()


    f = open(get_symbol_test_data_path(_symbol, _timeSeries, _timeInterval), 'w')
    testCSV = csv.writer(f)

    for line in testLines:
        testCSV.writerow(line)

    f.close()

'''
    Loads split data files.
'''
#tested
def load_split_data (_symbol, _timeSeries, _timeInterval, _testPercentage):
    # split data
    split_data(_symbol, _timeSeries, _timeInterval, _testPercentage)

    # load data and calculate input and output data
    trainInputs, trainOutputs = load_data(_symbol + '-TRAINSPLIT', _timeSeries, _timeInterval)
    testInputs, testOutputs = load_data(_symbol + '-TESTSPLIT', _timeSeries, _timeInterval)

    # randomize training data only. keep testing (trading) data in order
    train = list(zip(trainInputs, trainOutputs))
    random.shuffle(train)
    trainInputs, trainOutputs = zip(*train)

    # don't randomize testing data so we can simulate real trading

    return trainInputs, trainOutputs, testInputs, testOutputs
