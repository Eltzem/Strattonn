from Chromosome import Chromosome
from DNN import DNN

from Paths import get_path_slash

import random
import os
import os.path

#TODO: add in getting data for self.symbol to train with

class GeneticSearchDNN:


    def __init__ (self, _popSize, _selection, _mutation, _newblood, _crossoverPairs, _symbol, _testPercentage=0.1):

        # check whether search settings make sense
        if not self.verify_search_settings (_popSize, _selection, _mutation, _newblood, _crossoverPairs):
            raise Exception ('Genetic Search __init__(): search settings do not agree')

        self.popSize = _popSize
        self.selection = _selection
        self.mutation = _mutation
        self.newblood = _newblood
        self.crossoverPairs = _crossoverPairs

        self.symbol = _symbol # symbol to train data on

        self.testPercentage = _testPercentage # percentage of data to use for testing



    def searchVerbose (self, _numberToSave, _generations, _epochs, _batchSize, _initialPopulation = None):

        # get training/testing data
        trainInputs, trainOutputs, testInputs, testOutputs = self.load_training_and_testing_data(self.symbol)

        # initialize starting random Chromosomes
        chromosomes = []
        for x in range(self.popSize):
            chromosomes.append(Chromosome())

        # if you want to start with a list of Chromosomes, pass them in with _initialPopuation
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
                newDNN.compile(newDNN.optimizer, 'mean_squared_error')
                newDNN.train(trainInputs, trainOutputs, _epochs, _batchSize)
                
                losses.append(newDNN.evaluate(testInputs, testOutputs))
                print('\ntrained model:', x, 'with loss:', losses[len(losses)-1], '\n')
                dnns.append(newDNN)

                # save model
                #if not os.path.exists('search-dnn-saves' + get_path_slash() + str(generationCount)):
                #    os.mkdir('search-dnn-saves' + get_path_slash() + str(generationCount))

                #newDNN.save('search-dnn-saves' + get_path_slash() + str(generationCount) + get_path_slash() + \
                #            str(losses[x]) + 'fitness_chromosome-' + str(x))

                #newDNN.close()

            # aggregate all DNN data (loss, dnn, chromosome) into a list of tuples
            print('aggregating model performance data')
            models = []
            for x in range(len(dnns)):
                # add data to list of tuples for sorting
                models.append((losses[x], chromosomes[x], dnns[x]))
                print('model for generation', generationCount, 'has loss', models[x][0])
                print('mode:', models[x][1])

            # sort models based on loss
            print('\nsorting models by loss\n')
            models = sorted(models, key=get_sorted_key)
            
            # save models
            print('\nsaving', _numberToSave, 'best models\n')
            self.save_best_models(models, _numberToSave, 'search-dnn-saves' + get_path_slash() + str(generationCount))

            # close models to prevent errors
            for dnn in dnns:
                dnn.close()

            # Prepare Next Generation

            # new generation
            newChromosomes = []

            # selection
            for x in range(self.selection):
                print('\nadding selection\n')
                # choose index to select
                newChromosomes.append(chromosomes[self.tournament_selection(self.popSize)])
                print('added:', newChromosomes[len(newChromosomes)-1])
            
            # mutation
            for x in range(self.mutation):
                print('\nadding mutation\n')
                # choose index to mutate
                index = self.tournament_selection(self.popSize)

                # copy Chromosome before mutation
                newChromosome = Chromosome(_genome=chromosomes[index].get_genome_copy())

                # mutate new Chromosome
                newChromosome.mutate()

                print('existing:', chromosomes[index])
                
                # add new Chromosome
                newChromosomes.append(newChromosome)

                print('added:', newChromosomes[len(newChromosomes)-1])
                print('existing:', chromosomes[index])

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
                newChromosomes.append(Chromosome())
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

        return Chromosome(_genome=newGenome)

    def tournament_selection (self, _max):
        a = random.randint(0, _max - 1)
        b = random.randint(0, _max - 1)

        if a < b:
            return a
        return b

    # returns training and testing data for network. Randomizes it.
    def load_training_and_testing_data (self, _symbol):
        #TODO: inputs, outputs = loadData(_symbol)

        # just use dummy data for now
        inputs = [[3, 4, 5, 6, 7], [6, 7, 8, 9, 10], [2, 3, 4, 5, 6], [5, 6, 7, 8, 9], [1, 2, 3, 4, 5], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [2, 3, 4, 5, 6], [6, 7, 8, 9, 10], [4, 5, 6, 7, 8], [6, 7, 8, 9, 10], [0, 1, 2, 3, 4], [6, 7, 8, 9, 10], [5, 6, 7, 8, 9], [6, 7, 8, 9, 10], [6, 7, 8, 9, 10], [5, 6, 7, 8, 9], [6, 7, 8, 9, 10], [6, 7, 8, 9, 10], [4, 5, 6, 7, 8], [5, 6, 7, 8, 9], [5, 6, 7, 8, 9], [2, 3, 4, 5, 6], [6, 7, 8, 9, 10], [0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [4, 5, 6, 7, 8], [3, 4, 5, 6, 7], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [3, 4, 5, 6, 7], [2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [6, 7, 8, 9, 10], [0, 1, 2, 3, 4], [6, 7, 8, 9, 10], [3, 4, 5, 6, 7], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [3, 4, 5, 6, 7], [3, 4, 5, 6, 7], [1, 2, 3, 4, 5], [3, 4, 5, 6, 7], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [5, 6, 7, 8, 9], [6, 7, 8, 9, 10], [4, 5, 6, 7, 8], [3, 4, 5, 6, 7], [6, 7, 8, 9, 10], [4, 5, 6, 7, 8], [2, 3, 4, 5, 6], [5, 6, 7, 8, 9], [2, 3, 4, 5, 6], [6, 7, 8, 9, 10], [1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [5, 6, 7, 8, 9], [2, 3, 4, 5, 6], [6, 7, 8, 9, 10], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [5, 6, 7, 8, 9], [1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [6, 7, 8, 9, 10], [0, 1, 2, 3, 4], [4, 5, 6, 7, 8], [3, 4, 5, 6, 7], [6, 7, 8, 9, 10], [2, 3, 4, 5, 6], [2, 3, 4, 5, 6], [4, 5, 6, 7, 8], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [5, 6, 7, 8, 9], [5, 6, 7, 8, 9], [2, 3, 4, 5, 6], [6, 7, 8, 9, 10], [0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [0, 1, 2, 3, 4], [4, 5, 6, 7, 8], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [2, 3, 4, 5, 6], [5, 6, 7, 8, 9], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [1, 2, 3, 4, 5], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [0, 1, 2, 3, 4], [6, 7, 8, 9, 10], [6, 7, 8, 9, 10], [5, 6, 7, 8, 9], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [3, 4, 5, 6, 7], [1, 2, 3, 4, 5], [0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [6, 7, 8, 9, 10], [6, 7, 8, 9, 10], [5, 6, 7, 8, 9], [4, 5, 6, 7, 8], [2, 3, 4, 5, 6], [0, 1, 2, 3, 4], [3, 4, 5, 6, 7], [6, 7, 8, 9, 10], [6, 7, 8, 9, 10], [2, 3, 4, 5, 6], [6, 7, 8, 9, 10], [3, 4, 5, 6, 7], [6, 7, 8, 9, 10], [5, 6, 7, 8, 9]]

        outputs = [[8], [11], [7], [10], [6], [9], [9], [7], [11], [9], [11], [5], [11], [10], [11], [11], [10], [11], [11], [9], [10], [10], [7], [11], [5], [6], [9], [8], [7], [8], [8], [7], [5], [6], [11], [11], [5], [11], [8], [7], [8], [9], [7], [5], [6], [8], [9], [8], [8], [6], [8], [6], [6], [10], [11], [9], [8], [11], [9], [7], [10], [7], [11], [6], [11], [10], [7], [11], [8], [9], [9], [7], [5], [9], [9], [10], [6], [11], [11], [5], [9], [8], [11], [7], [7], [9], [6], [6], [6], [10], [10], [7], [11], [5], [10], [6], [11], [5], [9], [6], [6], [7], [7], [10], [8], [9], [6], [9], [9], [5], [11], [11], [10], [9], [9], [9], [8], [6], [5], [6], [8], [9], [9], [9], [9], [11], [11], [10], [9], [7], [5], [8], [11], [11], [7], [11], [8], [11], [10]]

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
            _models[modelIndex][2].save(str(modelIndex) + '-fitness_' + str(_models[modelIndex][0]))
            modelIndex += 1

        # restore old current working directory
        os.chdir(oldPath)

    # checks if search-wide variables make sense
    def verify_search_settings (self, _popSize, _selection, _mutation, _newblood, _crossoverPairs):

        if _popSize < 0 or _selection < 0 or _mutation < 0 or _newblood < 0 or _crossoverPairs < 0:
            return False
        if _selection + _mutation + _newblood + (_crossoverPairs * 2) != _popSize:
            return False

        return True

    # returns maing loss metric for DNN object with test inputs/outputs. Fitness of 0 is good, means 0 loss!
    def get_dnn_fitness (self, _dnn, _inputs, _outputs):
        return _dnn.evaluate(_inputs, _outputs)[0]

# helps with sorting tuples that hold a population
def get_sorted_key (item):
    return item[0]
