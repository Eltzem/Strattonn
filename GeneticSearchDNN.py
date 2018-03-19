#TODO: add crossover, mutation functions. maybe put these in Chromosome class

from Chromosome import Chromosome
from DNN import DNN

from Paths import get_path_slash

import random
import os
import os.path

class GeneticSearchDNN:


    def __init__ (self, _popSize, _selection, _mutation, _newblood, _crossoverPairs, _generations, _symbol, _testPercentage=0.1):

        # check whether search settings make sense
        if not self.verifySearchSettings (_popSize, _selection, _mutation, _newblood, _crossoverPairs, _generations):
            raise Exception ('Genetic Search __init__(): search settings do not agree')

        self.popSize = _popSize
        self.selection = _selection
        self.mutation = _mutation
        self.newblood = _newblood
        self.crossoverPairs = _crossoverPairs
        self.generations = _generations

        self.symbol = _symbol # symbol to train data on

        self.testPercentage = _testPercentage # percentage of data to use for testing



    def searchVerbose (self, _numberToSave, _epochs, _batchSize):

        # get training/testing data
        trainInputs, trainOutputs, testInputs, testOutputs = self.loadTrainingAndTestingData(self.symbol)

        # initialize starting random Chromosomes
        chromosomes = []
        for x in range(self.popSize):
            chromosomes.append(Chromosome())


        # loop through generations
        for generationCount in range(self.generations):
            print('\n==========\nStarting New Generation:', generationCount, '\n==========\n')

            dnns = []
            losses = []
            # create, train, and evaluate DNNs
            for x in range(len(chromosomes)):
                newDNN = DNN(_chromosome=chromosomes[x])
                newDNN.compile(newDNN.optimizer, 'mean_squared_error')
                newDNN.train(trainInputs, trainOutputs, _epochs, _batchSize)
                
                losses.append(newDNN.evaluate(testInputs, testOutputs))
                print('\ntrained model:', x, 'with loss:', losses[len(losses)-1], '\n')
                dnns.append(newDNN)

                # save model
                if not os.path.exists('search-dnn-saves' + get_path_slash() + str(generationCount)):
                    os.mkdir('search-dnn-saves' + get_path_slash() + str(generationCount))

                newDNN.save('search-dnn-saves' + get_path_slash() + str(generationCount) + get_path_slash() + \
                            str(losses[x]) + 'fitness_chromosome-' + str(x))

                newDNN.close()

            # aggregate all DNN data (loss, dnn, chromosome) into a list of tuples
            models = []
            for x in range(len(dnns)):
                # add data to list of tuples for sorting
                models.append((losses[x], dnns[x], chromosomes[x]))
                print('model for generation', generationCount, 'has loss', models[x][0])

            # sort models based on loss
            models = sorted(models, key=getSortedKey)
            
            # save models
            #print('\nsaving', _numberToSave, 'best models\n')
            #self.saveBestModels(models, _numberToSave, 'search-dnn-saves' + get_path_slash() + str(generationCount))

            # close models to prevent errors
            #for dnn in dnns:
            #    dnn.close()

            # TODO: prepare next generation

    # returns training and testing data for network. Randomizes it.
    def loadTrainingAndTestingData (self, _symbol):
        #TODO: inputs, outputs = loadData(_symbol)

        # just use dummy data for now
        inputs = [[0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4]] 

        outputs = [[3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423], [3.423]] 
        
        # randomize data
        data = list(zip(inputs, outputs))
        random.shuffle(data)
        inputs, outputs = zip(*data)

        # index to split training and testing data on
        indexDivider = int(len(inputs) * self.testPercentage)

        # split data
        testInputs = inputs[:indexDivider]
        testOutputs = outputs[:indexDivider]

        trainInputs = inputs[indexDivider:]
        trainOutputs = outputs[indexDivider:]

        return trainInputs, trainOutputs, testInputs, testOutputs

    # saves the best models of a generation to disk. Assumes _models is sorted
    def saveBestModels (self, _models, _numberToSave, _directoryPath):
        # save old current working directory
        oldPath = os.getcwd()
        
        # check if path exists. if not, create it
        if not os.path.exists(_directoryPath):
            os.mkdir(_directoryPath)
        os.chdir(_directoryPath)

        # save models in there
        modelIndex = 0
        while modelIndex < _numberToSave and modelIndex < len(_models):
            # save model with example name: 0-fitness_0.034234123141234
            _models[modelIndex][1].save(str(modelIndex) + '-fitness_' + str(_models[modelIndex][0]))
            modelIndex += 1

        # restore old current working directory
        os.chdir(oldPath)

    # checks if search-wide variables make sense
    def verifySearchSettings (self, _popSize, _selection, _mutation, _newblood, _crossoverPairs, _generations):

        if _popSize < 0 or _selection < 0 or _mutation < 0 or _newblood < 0 or _crossoverPairs < 0 or _generations <= 0:
            return False
        if _selection + _mutation + _newblood + (_crossoverPairs * 2) != _popSize:
            return False

        return True

    # returns maing loss metric for DNN object with test inputs/outputs. Fitness of 0 is good, means 0 loss!
    def getDNNFitness (self, _dnn, _inputs, _outputs):
        return _dnn.evaluate(_inputs, _outputs)[0]

# helps with sorting tuples that hold a population
def getSortedKey (item):
    return item[0]
