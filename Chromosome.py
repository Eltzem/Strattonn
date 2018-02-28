'''
[window size, inputs per window, optimizer, learning_rate, n_hl1, activation_hl1, dropout_hl1, n_hl2, activation_hl2, dropout_hl2, n_hl3, activation_hl3, dropout_hl3, n_hl4, activation_hl4, dropout_hl4, n_hl5, activation_hl5, dropout_hl5, n_hl5, activation_hl5, dropout_hl5, n_hl6, activation_hl6, dropout_hl6, n_hl7, activation_hl7, dropout_hl7, output_size, activation_output]
'''

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
    '''

    def __init__ (self, _list=None, _hlSizes=None, _hlActivations=None, _hlDropouts=None, _maxHL = 7):
        self.genome = []
        
        # Parameters for genome values

        self.maxHiddenLayers = _maxHL
        self.HIDDEN_LAYER_START = 4 # first index of hidden layer information

        self.minWindowCount = 1
        self.maxWindowCount = 20 # arbitrary max

        self.inputsPerWindow = 5 # hour, minute, ln() - ln(), trendline, volume

        self.minPerceptrons = 1
        self.maxPerceptrons = 10000 # arbitrary max

        self.minDropout = 0
        self.maxDropout = 1

        self.possibleOptimizers = ['sgd', 'rmsprop', 'adagrad', 'adadelta', 'adam', 'adamax', 'nadam']
        
        self.minLearningRate = 0.00001 # arbitrary min
        self.maxLearningRate = 1 # arbitrary max
        
        self.possibleActivations = ['softmax', 'elu', 'selu', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', \
                        'hard_sigmoid', 'linear']

        self.outputSize = 1

        # Initialize random genome

        self.genome.append(random.randint(self.minWindowCount, self.maxWindowCount))
        self.genome.append(self.inputsPerWindow)
        self.genome.append(random.choice(self.possibleOptimizers))
        self.genome.append(random.random() * self.maxLearningRate + self.minLearningRate)

        for x in range(self.maxHiddenLayers):
            # add hidden layer size from _hlSizes or random value
            if _hlSizes != None and x < len(_hlSizes):
                self.genome.append(_hlSizes[x])
            else:
                self.genome.append(random.randint(self.minPerceptrons, self.maxPerceptrons))
            
            # add hidden layer activation from _hlActivations or random valuei
            if _hlActivations != None and x < len(_hlActivations):
                self.genome.append(_hlActivations[x])
            else:
                self.genome.append(random.choice(self.possibleActivations))
            
            # add hidden layer dropout from _hlDropouts or random value
            if _hlDropouts != None and x < len(_hlDropouts):
                self.genome.append(_hlDropouts[x])
            else:
                self.genome.append(random.random() * self.maxDropout + self.minDropout)

        # output size
        self.genome.append(self.outputSize)
        # output activation function
        self.genome.append(random.choice(self.possibleActivations))

        # if a genome was passed in, use it instead
        if _genome != None:
            self.genome = _genome

    '''
        Returns string representation of the chromosome.
    '''
    def __str__ (self):
        return str(self.genome)

    # getters for actual data held in genome

    '''
        Cleans up the hidden layers in a genome. It 'slides' hidden layers to the left, so any layer
        with size 0 that don't exist are kept on the right side of the genome.
    '''

    def _format_genome (self):
        newGenome = []

        # add data before hidden layers
        for x in range(self.HIDDEN_LAYER_START):
            newGenome.append(newGenome[x])

        # add hidden layers
        sizes, activations, dropouts = self.hidden_layers()

        for x in range(len(sizes)):
            newGenome.append(sizes[x])
            newGenome.append(activations[x])
            newGenome.append(dropouts[x])

        # add 'null' data to end of hidden layer genome space
        for x in range(len(sizes), self.maxHiddenLayers):


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
            print(self.genome[x])
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
        return self.min_window_count()

    def max_window_count (self):
        return self.max_window_count()

    def inputs_per_window (self):
        return self.inputsPerWindow

    def min_perceptrons (self):
        return self.minPerceptrons

    def max_perceptrons (self):
        return self.maxPerceptrons

    def min_dropout (self):
        return self.min_dropout

    def max_dropout (self):
        return self.max_dropout

    def min_learning_rate (self):
        return self.minLearningRate

    def max_learning_rate (self):
        return self.maxLearningRate

    def output_size (self):
        return self.outputSize
