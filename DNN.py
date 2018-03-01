from keras.models import Sequential
from keras.layers import *
from keras import backend as KerasBackend

from DNN_dao import DNN_dao

import numpy as np

class DNN:

    # creates a blank model
    def __init__ (self, _chromosome=None, _saveDirectory=None):

        self.init_blank_model()

        # create from a chromosome if one was specified
        if _chromosome != None:
            self.init_from_chromosome(_chromosome)

        # create from a saved chromosome and model weights
        if _savefile=None:
            dao = DNN_dao()
            try:
                dao.load(_saveDirectory)
                self.init_from_chromosome(dao.chromosome())
                self.model = dao.model()
            # failed to load model somehow. init a blank model
            except Exception as e:
                print('FAILED to load saved DNN! Creating a blank one.')
                self.init_blank_model()

    # creates a blank model
    def init_blank_model (self):
        self.model = Sequential() # blank model
        self.layers = []

        # these values are useless unless set from a Chromosome
            # I initialize them here to avoid errors
        self.optimizer = 'adam'
        self.learningRate = 0.001
        self.windowSize = 1
        self.inputsPerWindow = 1

    # creates a model based off a Chromosome
    def init_from_chromosome (self, _chromosome):
        inputSize = _chromosome.input_size()
        optimizer = _chromosome.optimizer()
        learningRate = _chromosome.learning_rate()
        outputSize = _chromosome.output_size()
        outputActivation = _chromosome.output_activation()

        windowSize = _chromosome.window_size()
        inputsPerWindow = _chromosome.inputs_per_window()


        hl_sizes, hl_activations, hl_dropouts = _chromosome.hidden_layers()

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

    def close (self):
        self.model = None
        self.layers = None
        KerasBackend.clear_session()

    def add_dense (self, _perceptrons, _activation, _inputs=None, _dropoutRate=0):
        print("adding dense perceptron layer")

        newLayer = Dense(_perceptrons, activation=_activation, input_shape=(_inputs,))

        self.model.add(newLayer)
        self.layers.append(newLayer)

        # add Dropout to layer, if any
        if _dropoutRate > 0:
            self.add_dropout(_dropoutRate)

    def add_dropout (self, _dropoutRate):
        print("adding dropout")

        # dropout of a layer functions as a layer in Keras
        newLayer = Dropout(_dropoutRate)
        self.model.add(newLayer)
        self.model.layers.append(newLayer)

    # configure the learning process before training
    def compile (self, _optimizer, _loss, _metrics):
        print("compiling model")

        self.model.compile(optimizer=_optimizer, loss=_loss, metrics=_metrics)

    # fit model, I called it train
    def train (self, _inputs, _outputs, _epochs, _batchSize):
        print("training model")

        # make sure inputs and ouputs are numpy.array (s)
        _inputs = np.array(_inputs)
        _outputs = np.array(_outputs)

        self.model.fit(x=_inputs, y=_outputs, epochs=_epochs, batch_size=_batchSize, verbose=2)

    # test the model
    def evaluate (self, _inputs, _outputs):
        # make sure inputs and outputs are numpy.array (s)
        _inputs = np.array(_inputs)
        _outputs = np.array(_outputs)

        return self.model.evaluate(x=_inputs, y=_outputs)

    def predict (self, _inputs):
        # make sure inputs are numpy.array (s)
        _inputs = np.array(_inputs)

        # returns prediction as a single array
            # NOTE: this may not work if we change the number of outputs. This is a 'cheat,' and the system may not behave
            # like I think it does

        return self.model.predict(x=_inputs)[0]

    def get_layers(self):
        return self.layers
