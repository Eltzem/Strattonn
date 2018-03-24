from Chromosome import Chromosome
from DNN import DNN

from Paths import get_path_slash

import random
import os
import os.path

#TODO: add in getting data for self.symbol to train with

class GeneticSearchDNN:


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



    def searchVerbose (self, _saveDirectory, _numberToSave, _generations, _epochs, _batchSize, _initialPopulation = None, _maxHL=None):

        # get training/testing data
        trainInputs, trainOutputs, testInputs, testOutputs = self.load_training_and_testing_data()

        # initialize starting random Chromosomes
        chromosomes = []
        for x in range(self.popSize):
            newChromosome = Chromosome()
            #print('inputs:', newChromosome.input_size())
            chromosomes.append(Chromosome(_maxHL=_maxHL))

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

                print('dnn:', newDNN.get_model().summary())

                # NOTE: modified for MNIST
                newDNN.compile(newDNN.optimizer, 'categorical_hinge', _metrics=['categorical_accuracy'])
                newDNN.train(trainInputs, trainOutputs, _epochs, _batchSize)
                
                losses.append(newDNN.evaluate(testInputs, testOutputs)[1])
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
            
            # NOTE: added for MNIST
            # reverse sorted order
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
                newChromosome = Chromosome(_genome=chromosomes[index].get_genome_copy(), _maxHL=4)

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

    # returns training and testing data for network. Randomizes it.
    # NOTE: using MNIST data
    def load_training_and_testing_data (self):
        inputs, outputs = self.load_data()
        inputs = inputs.tolist()
        outputs = outputs.tolist()

        # randomize data
        data = list(zip(inputs, outputs))
        random.shuffle(data)
        inputs, outputs = zip(*data)

        # index to split training and testing data on
        indexDivider = int(len(inputs) * self.testPercentage)
        #print('indexDivider:', indexDivider)
        testInputs = []
        testOutputs = []

        # split data
        testInputs = inputs[:indexDivider]
        testOutputs = outputs[:indexDivider]

        trainInputs = inputs[indexDivider:]
        trainOutputs = outputs[indexDivider:]

        print('testInputs:', len(testInputs))
        print('testOutputs:', len(testOutputs))
        print('trainInputs:', len(trainInputs))
        print('trainOutputs:', len(trainOutputs))

        #print(testInputs[2])
        #print(testOutputs[2])
        #print(trainInputs[2])
        #print(trainOutputs[2])

        return trainInputs, trainOutputs, testInputs, testOutputs

    # NOTE: load MNIST data
    def load_data (self):
        # retrieve mnist data
        from keras.datasets import mnist
        (input_train, output_train), (input_test, output_test) = mnist.load_data()

        #print(input_train)

        '''
        inputs = input_train
        for elemenet in input_test:
            inputs.append(element)
        outputs = output_train
        for element in output_test:
            outputs.append(output_test)
        '''

        inputs = input_train.tolist() + input_test.tolist()
        outputs = output_train.tolist() + output_test.tolist()
        
        # flatten itmages (preprocessing)
        print('flattening images')
        from mnist import flatten_images
        inputs = flatten_images(inputs)
        print(inputs)

        # expand outputs into 10 categories (preprocessing)
        print('expanding outputs')
        from mnist import expand_outputs
        outputs = expand_outputs(outputs)
        print(outputs)


        print('inputs:', len(inputs))
        print('outputs:', len(outputs))
        return inputs, outputs

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
