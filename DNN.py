from keras.models import Sequential
from keras.layers import *
from keras import backend as KerasBackend

from DNN_dao import DNN_dao

import numpy as np

class DNN:

    # creates a blank model
    def __init__ (self, _chromosome=None, _saveDirectory=None):

        self.init_blank_model()

        self.chromosome=_chromosome

        # create from a chromosome if one was specified
        if _chromosome != None:
            self.init_from_chromosome(_chromosome)

        # create from a saved chromosome and model weights
        if _saveDirectory != None:
            try:
                self.load(_saveDirectory)
            # failed to load model somehow. init a blank model
            except Exception as e:
                print('FAILED to load saved DNN! Creating a blank one.')
                self.init_blank_model()


      
    '''
        Creates a blank model with no layers.
    '''
    def init_blank_model (self):
        self.model = Sequential() # blank model
        #self.layers = []

        # these values are useless unless set from a Chromosome
            # I initialize them here to avoid errors
        self.optimizer = 'adam'
        self.learningRate = 0.001
        self.windowSize = 1
        self.inputsPerWindow = 1

    '''
        Translates a Chromosome object into a neural network.
    
        Args:   _chromosome = Chromosome object to translate
    '''
    # creates a model based off a Chromosome
    def init_from_chromosome (self, _chromosome):
        self.model = Sequential() # blank model
        #self.layers = []

        print(_chromosome)

        inputSize = _chromosome.input_size()
        optimizer = _chromosome.optimizer()
        learningRate = _chromosome.learning_rate()
        outputSize = _chromosome.output_size()
        outputActivation = _chromosome.output_activation()

        windowSize = _chromosome.window_size()
        inputsPerWindow = _chromosome.inputs_per_window()


        hl_sizes, hl_activations, hl_dropouts = _chromosome.hidden_layers()
        #print('\n\n\nINPUT SIZE:', inputSize, '\n\n\n')
        # add inputs
        self.add_dense(hl_sizes[0], hl_activations[0], _inputs = inputSize, _dropoutRate = hl_dropouts[0])

        # add other hidden layers
        for x in range(1, len(hl_sizes)):
            self.add_dense(hl_sizes[x], hl_activations[x], _dropoutRate = hl_dropouts[x])

        # add output
        self.add_dense(outputSize, outputActivation)

        # save this information for use later
        self.optimizer = optimizer
        self.learningRate = learningRate
        self.windowSize = windowSize
        self.inputsPerWindow = inputsPerWindow

    '''
        Saves the DNN using the DAO object.

        Args:   _saveDirectory = directory to save the DNN items (DNN + Chromosome)
    '''
    def save (self, _saveDirectory):
        dao = DNN_dao()

        try:
            dao.save(_saveDirectory, self)
        except Exception as e:
            raise e

    '''
        Loads a saved DNN and Chromosome (if it exists).

        Args:   _saveDirectory = directory to load DNN items from (DNN + Chromosome)
    '''
    def load(self, _saveDirectory):
        dao = DNN_dao()

        # load
        try:
            dao.load(_saveDirectory)
        except Exception as e:
            raise e

        # get loaded data
        model = dao.get_model()
        # load chromosome if there was one
        chromosome = None
        try:
            chromosome = dao.get_chromosome()
        except Exception as e:
            print(str(e))

        # initialize from chromosome
        if chromosome != None:
            self.init_from_chromosome(chromosome)

        # create model. won't contain self.layers layer information without a chromosome
        self.model = model
        self.chromosome = chromosome
    
    '''
        'Closes' a model. This prevents sometimes random errors when utilizing a model.
    '''
    def close (self):
        self.model = None
        KerasBackend.clear_session()

    '''
        Adds a fully connected perceptron layer.

        Args:   _perceptrons = perceptrons to put in layer
                _activation = string, activation function for layer
                _inputs = number of inputs for layer (only use if this is the first layer)
                _dropoutRate = [0, 1), percentage of connections to 'dropout'
    '''
    def add_dense (self, _perceptrons, _activation, _inputs=None, _dropoutRate=0):
        #print("adding dense perceptron layer")

        newLayer = Dense(_perceptrons, activation=_activation, input_shape=(_inputs,))

        self.model.add(newLayer)
        #self.layers.append(newLayer)

        # add Dropout to layer, if any
        if _dropoutRate > 0:
            self.add_dropout(_dropoutRate)

    '''
        Leaves out some connections to and from this layer. Dropout helps prevent against
        over fitting.

        Args:   _dropoutRate = [0,1), percentage of connections to leave out
    '''
    def add_dropout (self, _dropoutRate):
        #print("adding dropout")

        # dropout of a layer functions as a layer in Keras
        newLayer = Dropout(_dropoutRate)
        self.model.add(newLayer)
        #self.model.layers.append(newLayer)

    '''
        Configures the learning process before the model is trained.

        Args:   _optimizer = string, optimizer to use for training
                _loss = string, loss metric to use
                _metrics = array of strings, addition loss metrics to display while training
    '''
    def compile (self, _optimizer, _loss, _metrics=None):
        print("compiling model")

        self.model.compile(optimizer=_optimizer, loss=_loss, metrics=_metrics)

    '''
        Trains the model with test data.

        Args:   _inputs = [ [0input0, 0input1, 0input2...], [1input0, 1input1, 1input2...]... ]
                _outputs = [ [0output0, 0output1, 0outptu2...], [1output0, 1output1, 1output2...]... ]
                _epochs = number of times to run through data while training
                _batchSize = number of input/output combinations to run though model before changing
                                weights
    '''
    def train (self, _inputs, _outputs, _epochs, _batchSize):
        print("training model")

        # make sure inputs and ouputs are numpy.array (s)
        _inputs = np.array(_inputs)
        _outputs = np.array(_outputs)

        self.model.fit(x=_inputs, y=_outputs, epochs=_epochs, batch_size=_batchSize, verbose=1)

    '''
        Test the model on non-training data.

        Args:   _inputs = inputs, same as defined in train()
                _outputs = outputs, same as defined in train()
                _directionalAccuracy = whether or not to include a percentage of times prediction
                                        is on the same side of 0 as the true output

        Returns:    array containing loss metric and additional loss metrics for training data
    '''
    def evaluate (self, _inputs, _outputs, _directionalAccuracy=False):
        # make sure inputs and outputs are numpy.array (s)
        _inputs = np.array(_inputs)
        _outputs = np.array(_outputs)

        evaluation = self.model.evaluate(x=_inputs, y=_outputs)
        return evaluation



    def evaluate_directional_accuracy (self, _inputs, _outputs):
        #print(_inputs)
        #print(_outputs)

        # loop through inputs and outputs. get predictions. see if ><0 matched ><0 of output
        numCorrect = 0

        for i in range(len(_inputs)):
            prediction = self.predict([_inputs[i]])
            #print('prediction:', prediction, 'expected:', _outputs[i][0])

            if (prediction > 0 and _outputs[i][0] > 0) or (prediction <= 0 and _outputs[i][0] <= 0):
                #print('correct')
                numCorrect += 1
            #else:
                #print('wrong')

        # calculate directional accuracy percentage correct
        percentageCorrect = numCorrect / len(_inputs)
        return percentageCorrect


    '''
        Predicts outputs for an input series.

        Args:   _inputs = [ [input0, input1, input2...] ] 2D ARRAY NEEDED!

        Returns:    array containing a predicted value for each output
    '''
    def predict (self, _inputs):
        # make sure inputs are numpy.array (s)
        _inputs = np.array(_inputs)

        # returns prediction as a single array
            # NOTE: this will not work if we change the number of outputs. This only returns the first
            # output of the model.
        #print(type(self.model.predict(x=_inputs)[0][0]))
        return self.model.predict(x=_inputs)[0][0]

    #def get_layers(self):
    #    return self.layers

    def get_model (self):
        return self.model

    def get_chromosome (self):
        return self.chromosome
