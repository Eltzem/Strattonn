import os
import os.path
import csv
import random

from GeneticSearchDNN import GeneticSearchDNN

'''
    Combines the input data for multiple stocks into one input series for a DNN.
    To use, find data files with the same length. For example, I've used length 3910.
    Put COPIES of all the CSV data files in a folder with that length.
    Run this file. It will generate files names ALL_input_data.csv and 
    ALL_output_data.csv. They will contain the aggregated input and output
    data for each time series. You can feed these rows and columns into a neural
    network. load_training_and_testing_data() loads this data for you and converts
    it to float values instead of strings.

    It uses aggregated data to try and predict stock price changes based on the price info
    of many companies, instead of one.
'''

def aggregate_data (_dataFolder):
    print('aggregating data files in folder with same number of row:', _dataFolder)

    inputs = []
    outputs = []

    for filename in os.listdir(_dataFolder):
        if '.csv' in filename and not '_' in filename and not 'MASTER' in filename and \
            not 'ALL' in filename:

            x, y = GeneticSearchDNN.load_data(filename[:-4], 'TIME_SERIES_INTRADAY', '1min')
            inputs.append(x)
            outputs.append(y)

    # aggregate inputs
    newcsv = csv.writer(open('data/1min/ALL_input_data.csv', 'w'))

    for timestamp in range(len(inputs[0])):
        newrow = []
        for symbol in inputs:
            for i in range(len(symbol[timestamp])):
                newrow.append(symbol[timestamp][i])


        newcsv.writerow(newrow)


def load_all_training_and_testing_data (_testPercentage, _outputSymbol, _dataFolder):
    aggregate_data(_dataFolder)

    print('loading training and testing data')

    csvI = csv.reader(open('data/1min/ALL_input_data.csv'))

    inputs = []

    # take out of csv

    for line in csvI:
        inputs.append(line)

    # convert to floats

    for line in inputs:
        for x in range(len(line)):
            line[x] = float(line[x])

    # retrieve output data
    inputsSymbol, outputs = GeneticSearchDNN.load_data(_outputSymbol, \
                                                                'TIME_SERIES_INTRADAY', '1min')

    # randomize data
    # NOTE: this is pretty much a copy of some stuff from
        # GeneticSearchDNN.load_training_and_testing_data(). It had to be done to bypass
        # the framePrepDnn and PreprocessCsv stuff that that method does. We need to use
        # custom preprocessing to aggregate input data.
    data = list(zip(inputs, outputs))
    random.shuffle(data)
    inputs, outputs = zip(*data)

    # index to split training and testing data on
    indexDivider = int(len(inputs) * _testPercentage)

    # split data
    trainInputs = inputs[indexDivider:]
    trainOutputs = outputs[indexDivider:]

    testInputs = inputs[:indexDivider]
    testOutputs = outputs[:indexDivider]

    return trainInputs, trainOutputs, testInputs, testOutputs

if __name__ == '__main__':
    trainInputs, trainOutputs, testInputs, testOutputs = load_all_training_and_testing_data(0.1, 'CTSH')
    print(len(trainInputs))
    #print(trainInputs)
    print(len(trainOutputs))
    print(len(testInputs))
    print(len(testOutputs))
    
    #print(testOutputs)
    print(len(testOutputs[3]))
