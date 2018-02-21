'''
[window size, optimizer, learning_rate, activation_input, dropout_input, n_hl1, activation_hl1, dropout_hl1, n_hl2, activation_hl2, dropout_hl2, n_hl3, activation_hl3, dropout_hl3, n_hl4, activation_hl4, dropout_hl4, n_hl5, activation_hl5, dropout_hl5, n_hl5, activation_hl5, dropout_hl5, n_hl6, activation_hl6, dropout_hl6, n_hl7, activation_hl7, dropout_hl7, activation_output]
'''

import random

class Chromosome:

    def __init__ (self):
        self.genome = []
        self.MAX_HIDDEN_LAYERS = 7


        self.minPerceptrons = 1
        self.maxPerceptrons = 10001 # arbitrary max

        self.minDropout = 0
        self.maxDropout = 1

        optimizers = ['sgd', 'rmsprop', 'adagrad', 'adadelta', 'adam', 'adamax', 'nadam']
        self.minLearningRate = 0.00001 # arbitrary min
        self.maxLearningRate = 1 # arbitrary max
        
        activations = ['softmax', 'elu', 'selu', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', \
                        'hard_sigmoid', 'linear']
        #TODO create random genome here

    def windowSize (self):
        return self.genome[0]

    def optimizer (self):
        return self.genome[1]

    def learningRate (self):
        return self.genome[2]

    def inputActivation (self):
        return self.genome[3]

    def inputDropout (self):
        return self.genome[4]

    def outputActivation (self):
        return self.genome(len(self.genome) - 1)

    def hiddenLayers (self):
        sizes = []
        activations = []
        dropouts = []

        # loop through layer information
        x = 5
        while x <= range(4, len(self.genome) - 2):
            # check if layer meets perceptron threshold to be considered
            if self.genome[x] >= self.minPerceptrons:
                # add info to layers
                sizes.append(self.genome[x])
                activations.append(self.genome[x+1])
                dropouts.append(self.genome[x+2])
            # increment to next layer
            x += 3

        return sizes, activations, dropouts
