'''
[window size, inputs per window, optimizer, learning_rate, n_hl1, activation_hl1, dropout_hl1, n_hl2, activation_hl2, dropout_hl2, n_hl3, activation_hl3, dropout_hl3, n_hl4, activation_hl4, dropout_hl4, n_hl5, activation_hl5, dropout_hl5, n_hl5, activation_hl5, dropout_hl5, n_hl6, activation_hl6, dropout_hl6, n_hl7, activation_hl7, dropout_hl7, output_size, activation_output]
'''

from Chromosome_dao import Chromosome_dao

import random

class Chromosome:

    '''
        Default constructor. Creates a random chromosome within certain bounds.

        Args:   list _genome: contains a new genome for the Chromosome to use
                list of integers _hlSizes: contains a list of integers representing hidden layer sizes
                list of strings _hlActivations: contains a list of strings representing activation
                                                functions
                list of floats _hlDropouts: contains a list of floats representing hidden layer 
                                                dropout rates
                integer _maxHL: maximum number of hidden layers (determines size of chromosome)
                string _filepath: path of file to load a Chromosome from
    '''

    def __init__ (self, _genome=None, _hlSizes=None, _hlActivations=None, _hlDropouts=None, \
                    _maxHL = 7):
        self.genome = []
       
        # Set Parameters for genome values

        self.maxHiddenLayers = _maxHL
        self.HIDDEN_LAYER_START = 4 # first index of hidden layer information

        # NOTE: modified for MNIST
        self.minWindowCount = 28
        self.maxWindowCount = 28# arbitrary max

        # NOTE: modified for MNIST
        self.inputsPerWindow = 28 # hour, minute, ln() - ln(), trendline, volume

        self.minPerceptrons = 1
        self.maxPerceptrons = 1000 # arbitrary max

        self.minDropout = 0
        self.maxDropout = 1

        self.possibleOptimizers = ['sgd', 'rmsprop', 'adagrad', 'adadelta', 'adam', 'adamax', 'nadam']
        
        self.minLearningRate = 0.00001 # arbitrary min
        self.maxLearningRate = 1 # arbitrary max
        
        self.possibleActivations = ['softmax', 'elu', 'selu', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', \
                        'hard_sigmoid', 'linear']

        # NOTE: modified for MNIST
        self.outputSize = 10

        # Create random genome to start with at least
        self.init_random(_hlSizes=_hlSizes, _hlActivations=_hlActivations, _hlDropouts=_hlDropouts)

        # if a genome was passed in, use it instead
        if _genome != None:
            self.genome = _genome

        # format the genome!
        self._format_genome()

    '''
        Initializes a random Chromosome.
    '''
    def init_random (self, _hlSizes=None, _hlActivations=None, _hlDropouts=None):
        # Initialize random genome

        self.genome.append(self.random_window_count())
        self.genome.append(self.inputs_per_window())
        self.genome.append(self.random_optimizer())
        self.genome.append(self.random_learning_rate())

        for x in range(self.maxHiddenLayers):
            # add hidden layer size from _hlSizes or random value
            if _hlSizes != None and x < len(_hlSizes):
                self.genome.append(_hlSizes[x])
            else:
                self.genome.append(self.random_perceptron_count())

            # add hidden layer activation from _hlActivations or random valuei
            if _hlActivations != None and x < len(_hlActivations):
                self.genome.append(_hlActivations[x])
            else:
                self.genome.append(self.random_activation())
            
            # add hidden layer dropout from _hlDropouts or random value
            if _hlDropouts != None and x < len(_hlDropouts):
                self.genome.append(_hlDropouts[x])
            else:
                self.genome.append(self.random_dropout())

        self.HIDDEN_LAYER_END = len(self.genome) - 1 # save end of Hidden Layer sections. Right here the HL were the last thing added

        # output size
        self.genome.append(self.output_size())
        # output activation function
        self.genome.append(self.random_activation())

    def _format_genome (self):
        newGenome = []

        # add data before hidden layers
        for x in range(self.HIDDEN_LAYER_START):
            newGenome.append(self.genome[x])

        # add hidden layers
        sizes, activations, dropouts = self.hidden_layers()

        for x in range(len(sizes)):
            newGenome.append(sizes[x])
            newGenome.append(activations[x])
            newGenome.append(dropouts[x])

        # add 'null' data to end of hidden layer genome space
        for x in range(len(sizes), self.maxHiddenLayers):
            newGenome.append(0)
            newGenome.append('none')
            newGenome.append(0)

        # add output data to new genome
        for x in range(self.HIDDEN_LAYER_END + 1, len(self.genome)):
            newGenome.append(self.genome[x])

        self.genome = newGenome
    
    #tested 
    '''
        Load Chromosome from file.
    '''
    @staticmethod
    def load (_filepath):
        dao = Chromosome_dao()
        try:
            dao.load(_filepath)
        except Exception as e:
            raise e

        return dao.get_chromosome()

    #tested
    '''
        Save Chromosome.
    '''
    def save (self, _filepath):
        try:
            dao = Chromosome_dao()
            dao.save(self, _filepath)

        except Exception as e:
            raise e

    '''
        Returns the genome list.
    '''
    def get_genome (self):
        return self.genome

    '''
        Returns the genome list as a copy.
    '''
    def get_genome_copy (self):
        genomeCopy = []
        for element in self.genome:
            genomeCopy.append(element)

        return genomeCopy

    '''
        Returns string representation of the chromosome.
    '''
    def __str__ (self):
        return str(self.genome)

    # getters for actual data held in genome

    '''
        Cleans up the hidden layers in a genome. It 'slides' hidden layers to the left, so any layers
        with size 0 that don't exist are kept on the right side of the genome. It appends 'null' hidden
        layer information to the end of the genome hidden layer section.
    '''


    #tested
    '''
        Randomly changes one of the Chromosome values.

        NOTE: Assumes that this will never hit the recursion depth limit. I tested it 100 million times
        and it never did, so it's a pretty good assumption. Some elements of the Chromosome aren't
        allowed to be modified, so it will recursively call self.mutate() if one of those are selected
        for modification.
    '''
    def mutate (self):
        index = random.randint(0, len(self.genome) - 1)

        #print('mutation index:', index)

        newValue = None
        if index == 0:
            newValue = self.random_window_count()
        elif index == 1: # don't change the inputs_per_window value yet, or ever maybe, try to mutate again
            newValue = self.genome[1]
            self.mutate()
        elif index == 2:
            newValue = self.random_optimizer()
        elif index == 3:
            newValue = self.random_learning_rate()

        # hidden layer parameter
        elif index >= self.HIDDEN_LAYER_START and index <= self.HIDDEN_LAYER_END:
            # activation function
            if isinstance(self.genome[index], str):
                newValue = self.random_activation()

            # hidden layer size
                # relies on assumption that the next item in Chromosome after a hidden layer size is a string (activation function)
            elif isinstance(self.genome[index + 1], str):
                newValue = self.random_perceptron_count()

            # dropout
            else:
                newValue = self.random_dropout()

        elif index == self.HIDDEN_LAYER_END + 1: # don't change the output size, try to mutate again
            newValue = self.output_size()
            self.mutate()
        else:
            newValue = self.random_activation()

        #print('newValue:', newValue)

        # apply change
        self.genome[index] = newValue

    # these functions generate random values based on pre-defined value constraints

    def random_window_count (self):
        return random.randint(self.min_window_count(), self.max_window_count())

    def random_optimizer (self):
        return random.choice(self.possible_optimizers())

    def random_learning_rate (self):
        return random.random () * self.max_learning_rate() + self.min_learning_rate()

    def random_perceptron_count (self):
        return random.randint(self.min_perceptrons(), self.max_perceptrons())

    def random_activation (self):
        return random.choice(self.possible_activations())

    def random_dropout (self):
        return random.random() * self.max_dropout() + self.min_dropout()


    '''
        Returns genome.
    '''
    def get_genome (self):
        return self.genome

    '''
        Returns number of inputs in DNN.
    '''
    def input_size (self):
        return self.window_size() * self.inputs_per_window()

    '''
        Returns window size of the DNN. This is the number of time periods fed as inputs to the network.
    '''
    def window_size (self):
        return self.genome[0]

    '''
        Returns the number of inputs per window size of the DNN.
    '''

    def inputs_per_window (self):
        return self.genome[1]

    '''
        The optimizer used by the network. The optimizer controls the adjusting of weights.
    '''
    def optimizer (self):
        return self.genome[2]

    '''
        Returns the learning rate used by the optimizer to adjust weights.
    '''
    def learning_rate (self):
        return self.genome[3]

    '''
        Returns the number of outputs.
    '''
    def output_size (self):
        return self.genome[len(self.genome) - 2]

    '''
        Returns the activation function used on the output layer.
    '''
    def output_activation (self):
        return self.genome[len(self.genome) - 1]

    '''
        Returns 3 lists containing information about the hidden layers. If a hidden layer has no
        perceptrons, it is removed from this list.

        Returns:sizes = list containing perceptron counts
                activations = list containing activation functions
                dropouts = list containing dropout rates
    '''
    def hidden_layers (self):
        sizes = []
        activations = []
        dropouts = []

        # loop through layer information
        x = self.HIDDEN_LAYER_START
        while x <= len(self.genome) - 3:
            #print(self.genome[x])
            # check if layer meets perceptron threshold to be considered
            if self.genome[x] >= self.minPerceptrons:
                # add info to layers
                sizes.append(self.genome[x])
                activations.append(self.genome[x+1])
                dropouts.append(self.genome[x+2])
            # increment to next layer
            x += 3

        # check if no hidden layers are present, at least one is required
        # return one hidden layer
        if len(sizes) < 1:
            sizes = [1]
            activations = [self.genome[self.HIDDEN_LAYER_START + 1]]
            dropouts = [0]

        return sizes, activations, dropouts


    # simple getters for parameters for genome values

    def possible_optimizers (self):
        return self.possibleOptimizers

    def possible_activations (self):
        return self.possibleActivations

    def max_hidden_layers (self):
        return self.maxHiddenLayers

    def min_window_count (self):
        return self.minWindowCount

    def max_window_count (self):
        return self.maxWindowCount

    def inputs_per_window (self):
        return self.inputsPerWindow

    def min_perceptrons (self):
        return self.minPerceptrons

    def max_perceptrons (self):
        return self.maxPerceptrons

    def min_dropout (self):
        return self.minDropout

    def max_dropout (self):
        return self.maxDropout

    def min_learning_rate (self):
        return self.minLearningRate

    def max_learning_rate (self):
        return self.maxLearningRate

    def output_size (self):
        return self.outputSize