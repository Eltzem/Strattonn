from Chromosome import Chromosome
from DNN import DNN

from keras import backend as KerasBackend

from Paths import get_path_slash
from Paths import get_symbol_data_path
from Paths import get_symbol_data

from PreprocessCsv import PreprocessCsv
from framePrepDnn import framePrepDnn

from CreateAggregateInputOutputFiles import load_all_training_and_testing_data

import random
import os
import os.path

#TODO: add in getting data for self.symbol to train with

class GeneticSearchDNNAll:

    '''
        Initializes a GeneticSearchDNN object. Specify some main test parameters here.

        Args:   int _popSizes = population size
                int _selection = number selected each generation
                int _mutation = number mutated each generation
                int _newblood = number of newblood each generation
                int _crossoverPairs = number of pairs to be mated each generation
                float _testPercentage = (0, 1) ratio of total inputs and outputs to be used as test data
    '''
    def __init__ (self, _popSize, _selection, _mutation, _newblood, _crossoverPairs, _testPercentage=0.1):

        # check whether search settings make sense
        if not self.verify_search_settings (_popSize, _selection, _mutation, _newblood, _crossoverPairs):
            raise Exception ('Genetic Search __init__(): search settings do not agree')

        self.popSize = _popSize
        self.selection = _selection
        self.mutation = _mutation
        self.newblood = _newblood
        self.crossoverPairs = _crossoverPairs

        self.testPercentage = _testPercentage # percentage of data to use for testing


    '''
        Conducts a genetic search on Chromosome objects representing DNNs.

        Args:   string _saveDirectory = directory path to save best DNN and Chromosome objects for each generation
                int _numberToSave = number of the best DNN objects to save each generation
                int _generations = number of generation to conduct search for
                int _epochs = base number of epochs to train each DNN for
                int _batchSize = batch size for Keras training
                Chromosome[] _initialPopulation = list of Chromosomes to use as the initial population. Max hidden layer count
                                                    of each Chromosome must match _maxHL
                int _maxHL = maximum number of hidden layers each Chromosome can represent
                float _goodLoss = [0, 1) loss that a model become lower than to become considered 'good.' Good models will
                                    be trained more.
                float _goodDA = [0, 1] directional accuracy that a model must be higher than to become considered 'good.'
                                    Good models will be trained more.
    '''
    def searchVerbose (self, _symbol, _dataFolder,  _timeSeries, _timeInterval, _saveDirectory, \
                        _numberToSave, _generations, _epochs, _batchSize, _maxHL, \
                        _initialPopulation = None,  _goodLoss = 0, _goodDA = 1):

        # get training/testing data
        trainInputs, trainOutputs, testInputs, testOutputs =  \
            load_all_training_and_testing_data(self.testPercentage, _symbol, _dataFolder)

        # initialize starting random Chromosomes
        chromosomes = []
        for x in range(self.popSize):
            newChromosome = Chromosome()
            #print('inputs:', newChromosome.input_size())
            chromosomes.append(Chromosome(_maxHL=_maxHL))
        if _initialPopulation != None:
            chromosomes = _initialPopulation

        # loop through generations
        for generationCount in range(_generations):
            print('\n==========\nStarting New Generation:', generationCount, '\n==========\n')

            # Work with Current Generation

            dnns = []
            losses = []
            # create, train, and evaluate DNNs
            for x in range(len(chromosomes)):
                newDNN = DNN(_chromosome=chromosomes[x])

                print('dnn:', newDNN.get_model().summary())

                newDNN.compile(newDNN.optimizer, 'mean_squared_error')
                newDNN.train(trainInputs, trainOutputs, _epochs, _batchSize)
               
                loss, directionalAccuracy = self.get_dnn_fitness(newDNN, testInputs, testOutputs)
                losses.append([loss, directionalAccuracy])
                print('\ntrained model:', x, 'with loss:', loss, 'and directional accuracy:', \
                        directionalAccuracy, '\n')
                dnns.append(newDNN)

                # Extended training of 'good' models.
                # checks if loss is 'good'. If so, train the model some more.
                lastIndex = len(losses)-1
                if losses[lastIndex][0] < _goodLoss or losses[lastIndex][1] > _goodDA:
                    print('\nLoss is', losses[lastIndex][0], 'and directional accuracy is:', \
                            losses[lastIndex][1], '. Training some more.\n')

                    # train model more
                    newDNN.train(trainInputs, trainOutputs, _epochs * 3, int(_batchSize / 2))
                     
                    # change loss
                    loss, directionalAccuracy = self.get_dnn_fitness(newDNN, testInputs, testOutputs)
                    losses[lastIndex] = [loss, directionalAccuracy] 

                    print('\ntrained model:', x, 'with loss:', loss, 'and directional accuracy:', \
                            directionalAccuracy, '\n')


            # aggregate all DNN data (loss, dnn, chromosome) into a list of tuples
            print('aggregating model performance data')
            models = []
            for x in range(len(dnns)):
                # add data to list of tuples for sorting
                models.append((losses[x], chromosomes[x], dnns[x]))
                print('model for generation', generationCount, 'has loss', models[x][0])
                print('mode:', models[x][1])

            # sort models based on directional accuracy
            print('\nsorting models by directional accuracy\n')
            models = sorted(models, key=get_sorted_key)
            # reverse to use directional accuracy metric to sort, instead of error
            newModels = []
            for x in range(len(models)-1, -1, -1):
                newModels.append(models[x])
            models = newModels

            # save models
            print('\nsaving', _numberToSave, 'best models\n')
            # make sure save directory exists
            if not os.path.exists(_saveDirectory):
                os.mkdir(_saveDirectory)
            self.save_best_models(models, _numberToSave, _saveDirectory + get_path_slash() + str(generationCount))

            # close models to prevent errors
            for dnn in dnns:
                dnn.close()

            # Prepare Next Generation

            # new generation
            newChromosomes = []

            # selection
            selected = []
            for x in range(self.selection):
                print('\nadding selection\n')
                # choose index to select
                selection = self.tournament_selection(_max = self.popSize)
                while selection in selected:
                    selection = self.tournament_selection(_max = self.popSize)

                selected.append(selection)
                newChromosomes.append(chromosomes[x])
                print('added:', newChromosomes[len(newChromosomes)-1], 'index:', selection)
            
            # mutation
            for x in range(self.mutation):
                print('\nadding mutation\n')
                # choose index to mutate
                index = self.tournament_selection(self.popSize)

                # copy Chromosome before mutation
                newChromosome = Chromosome(_genome=chromosomes[index].get_genome_copy(), _maxHL=_maxHL)

                # mutate new Chromosome
                newChromosome.mutate()

                print('existing:', chromosomes[index])
                
                # add new Chromosome
                newChromosomes.append(newChromosome)

                print('added:', newChromosomes[len(newChromosomes)-1])
                #print('existing:', chromosomes[index])

            # crossover
            for x in range(self.crossoverPairs):
                print('\nadding crossover\n')
                
                # choose indeces to mate
                a = self.tournament_selection(self.popSize)
                b = self.tournament_selection(self.popSize)

                print('a:', chromosomes[a])
                print('b:', chromosomes[b])

                # add new crossovered Chromosomes
                newChromosomes.append(self.crossover(chromosomes[a], chromosomes[b]))
                print('added:', newChromosomes[len(newChromosomes)-1])
                newChromosomes.append(self.crossover(chromosomes[a], chromosomes[b]))
                print('added:', newChromosomes[len(newChromosomes)-1])

            # newblood
            for x in range(self.newblood):
                print('\nadding newblood\n')
                newChromosomes.append(Chromosome(_maxHL=_maxHL))
                print('added:', newChromosomes[len(newChromosomes)-1])
            

            # set chromosome popuation as newly created population
            chromosomes = newChromosomes

    '''
        Performs crossover on 2 Chromosomes.

        Args:   _a = Chromosome
                _b = Chromosome

        Returns:    A Chromosome that is the crossover product of _a and _b.
    '''
    def crossover (self, _a, _b):
        print('performing crossover')
        genomeA = _a.get_genome()
        genomeB = _b.get_genome()

        index = random.randint(0, len(genomeA) - 1)

        newGenome = genomeA[:index] + genomeB[index:]

        return Chromosome(_genome=newGenome, _maxHL=_a.max_hidden_layers())

    '''
        Uses a tournament selection formula to select a probably low number comapred to the max.

        Args:   int _max = maximum number that can be chosen. _max > 0

        Retunrs:int = number [0, _max]
    '''
    def tournament_selection (self, _max):

        options = []

        for x in range(int(_max * 0.05 + 1)):
            options.append(random.randint(0, _max-1))

        '''
        a = random.randint(0, _max - 1)
        b = random.randint(0, _max - 1)

        if a < b:
            return a
        return b
        '''

        return sorted(options)[0]

    '''
        Loads data for training and testing of models. Splits data so self.testPercentage is used as the percentage
        of data for testing.

        Returns:    4 lists. Each list contains the data described by the name in format: [ [0data0, 0data1, 0data2], [1data0, 1data1,
                    1data2], ...]
    '''

    # TODO: change these 2 functions to work with stock data once the inputs / outputs are ready

    # returns training and testing data for network. Randomizes it.
    @staticmethod
    def load_training_and_testing_data (_testPercentage, _symbol, _timeSeries, _timeInterval=None):
        print('loading training and testing data')

        inputs, outputs = GeneticSearchDNN.load_data(_symbol, _timeSeries, _timeInterval)

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


        print('trainInputs:', len(trainInputs))
        print('trainOutputs:', len(trainOutputs))
        print('testInputs:', len(testInputs))
        print('testOutputs:', len(testOutputs))

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

    @staticmethod
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
        Saves the best models of each generation.

        Args:   list _models = List of DNN objects that represents the generation. Should be sorted so 'best' models are near front
                                of list.
                int _numberToSave = number of best models to save
                _directory path = Path to store saved models for the generation
    '''
    # saves the best models of a generation to disk. Assumes _models is sorted
    def save_best_models (self, _models, _numberToSave, _directoryPath):
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
            _models[modelIndex][2].save(str(modelIndex) + '-loss_' + str(_models[modelIndex][0][0]) + 'da_' + \
                                        str(_models[modelIndex][0][1]))
            modelIndex += 1

        # restore old current working directory
        os.chdir(oldPath)

    '''
        Checks if the search settings specified in the constructor method work together.

        Args: Genetic Search parameters

        Returns:True/False  Search settings make sense/Search settings don't make sense
    '''
    # checks if search-wide variables make sense
    def verify_search_settings (self, _popSize, _selection, _mutation, _newblood, _crossoverPairs):

        if _popSize < 0 or _selection < 0 or _mutation < 0 or _newblood < 0 or _crossoverPairs < 0:
            return False
        if _selection + _mutation + _newblood + (_crossoverPairs * 2) != _popSize:
            return False

        return True

    # returns maing loss metric for DNN object with test inputs/outputs. Fitness of 0 is good, means 0 loss!
    def get_dnn_fitness (self, _dnn, _inputs, _outputs):
        loss = _dnn.evaluate(_inputs, _outputs) # assumes only 1 output
        directionalAccuracy = _dnn.evaluate_directional_accuracy(_inputs, _outputs)

        return loss, directionalAccuracy

# helps with sorting tuples that hold a population
def get_sorted_key (item):
    return item[0][1]
